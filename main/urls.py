"""gallery URL Configuration

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
from django.urls import path, include
from . import views
#from .views import UserDocsView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url


urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendar, name='calendar'),
    path('docs/', views.UserDocsView.as_view(template_name='main/docs.html'), name='docs'),
    path('categories/', views.UserCategoriesView.as_view(template_name='main/categories.html'), name='categories'),
    path('new_doc/', views.DocCreateView.as_view(), name='new_doc'),
    path('new_cat/', views.CategoryCreateView.as_view(), name='new_cat'),
    path('doc/<int:pk>/', views.DocDetailView.as_view(), name='doc_detail'),
    path('doc/<int:pk>/update/', views.DocUpdateView.as_view(), name='doc_update'),
    path('doc/<int:pk>/delete/', views.doc_delete, name='doc_delete'),
    path('cat/<int:pk>/', views.CategoryDetailView.as_view(), name='cat_detail'),
    path('cat/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='cat_update'),
    path('cat/<int:pk>/delete/', views.cat_delete, name='cat_delete')
]
    # path('doc/<int:pk>/delete/<str:view>/', views.doc_delete, name='doc_delete')]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# admin.site.site_header = 'Správa webu'
