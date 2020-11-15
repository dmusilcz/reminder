from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView
from django.utils import translation
from django.urls import translate_url
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import LoginForm, SignUpForm, UserInformationUpdateForm, ProfileUpdateForm
from .models import Profile

# Create your views here.


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
            self.request.session.set_expiry(30)
            self.request.session.modified = True
            print('Remember me checked')
        return super(UpdatedLoginView, self).form_valid(form)

    def get_success_url(self):
        url = super(UpdatedLoginView, self).get_success_url()
        user = self.request.user
        if user.is_authenticated:
            language = user.profile.language
            translation.activate(language)
            self.request.session[translation.LANGUAGE_SESSION_KEY] = language

        return url


@method_decorator(login_required, name='dispatch')
class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'users/my_account.html'

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False


@login_required
def user_update_view(request):
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
            messages.success(request, 'Account updated')
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


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('my_account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {'form': form})


def set_language_from_url(request, user_language):
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return redirect(request.META.get('HTTP_REFERER', 'home'))
