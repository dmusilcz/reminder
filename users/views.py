from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.utils import translation
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import LoginForm, SignUpForm, UserInformationUpdateForm, ProfileUpdateForm
from .models import Profile
from django.utils.translation import gettext_lazy as _


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            language = translation.get_language()
            request.session[translation.LANGUAGE_SESSION_KEY] = language
            profile = Profile.objects.create(user=user, language=language, news_consent=True)
            profile.save()

            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


class UpdatedLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']

        if remember_me:
            session_cookie_age = 60 * 60 * 24 * 14
            self.request.session.set_expiry(session_cookie_age)
            self.request.session.modified = True
        return super(UpdatedLoginView, self).form_valid(form)

    def get_success_url(self):
        url = super(UpdatedLoginView, self).get_success_url()
        user = self.request.user
        language = user.profile.language
        translation.activate(language)
        self.request.session[translation.LANGUAGE_SESSION_KEY] = language

        return url


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'users/my_account.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return super(UserDetailView, self).get(request, *args, **kwargs)
        else:
            return redirect('user_denied')

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False


@login_required
def user_update_view(request):
    if request.user.is_active:
        if request.method == 'POST':
            u_form = UserInformationUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                                       instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                user_language = request.user.profile.language
                translation.activate(user_language)
                request.session[translation.LANGUAGE_SESSION_KEY] = user_language
                messages.success(request, _('Account updated'))
                return redirect('my_account')

        else:
            u_form = UserInformationUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'checked': request.user.profile.news_consent
        }

        return render(request, 'users/my_account_update.html', context)
    else:
        return redirect('user_denied')


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return super(AccountDeleteView, self).get(request, *args, **kwargs)
        else:
            return redirect('user_denied')

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False


@login_required
def change_password(request):
    if request.user.is_active:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, _('Your password was successfully updated!'))
                return redirect('my_account')
            else:
                messages.error(request, _('Please correct the error below.'))
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'users/password_change.html', {'form': form})
    else:
        return redirect('user_denied')


def user_denied(request):
    return render(request, 'users/user_denied.html')


def set_language_from_url(request, user_language):
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    return redirect(request.META.get('HTTP_REFERER', 'home'))
