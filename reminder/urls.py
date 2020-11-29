"""reminder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    re_path(r'^signup/$', user_views.signup, name='signup'),
    re_path(r'^login/$', user_views.UpdatedLoginView.as_view(template_name='users/login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            email_template_name='users/password_reset_email.html',
            subject_template_name='users/password_reset_subject.txt'
        ),
        name='password_reset'),
    re_path(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    re_path(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
    re_path(r'^account/update/', user_views.user_update_view, name='my_account_update'),
    re_path(r'^account/', user_views.UserDetailView.as_view(), name='my_account'),
    re_path(r'^password/$', user_views.change_password, name='password_change'),
    re_path(r'^account_delete/$', user_views.AccountDeleteView.as_view(), name='account_delete'),
    re_path(r'^user_denied/$', user_views.user_denied, name='user_denied'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'set_language/(?P<user_language>\w+)/$', user_views.set_language_from_url, name="set_language_from_url"),
    path('', include('main.urls')),
]