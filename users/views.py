from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView

from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, SignUpForm, UserInformationUpdateForm, ProfileUpdateForm

# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    terms = render_to_string('main/includes/terms_of_use.html')
    policy = render_to_string('main/includes/privacy_policy.html')
    return render(request, 'users/signup.html', {'form': form,
                                                 'terms': terms,
                                                 'policy': policy})


class UpdatedLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if remember_me:
            self.request.session.set_expiry(30)
            self.request.session.modified = True
            print('Remember me checked')
        return super(UpdatedLoginView, self).form_valid(form)


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


# @method_decorator(login_required, name='dispatch')
# class UserUpdateView(UpdateView, UserPassesTestMixin):
#     form_class = UserInformationUpdateForm
#     template_name = 'users/my_account_update.html'
#     success_url = reverse_lazy('my_account')
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def test_func(self):
#         user = self.get_object()
#         if self.request.user == user:
#             return True
#         return False

@login_required
def user_update_view(request):
    if request.method == 'POST':
        u_form = UserInformationUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
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
