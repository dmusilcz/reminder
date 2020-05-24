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
from .forms import LoginForm, SignUpForm, UserInformationUpdateForm

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
        remember_me = form.cleaned_data['remember_me']  # get remember me data from cleaned_data of form
        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is
            self.request.session.modified = True
            print('Remember me unchecked')
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


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView, UserPassesTestMixin):
    form_class = UserInformationUpdateForm
    template_name = 'users/my_account_update.html'
    success_url = reverse_lazy('my_account')

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False
