from django.contrib import admin

# Register your models here.

from .models import Category, Document

admin.site.register(Category)
admin.site.register(Document)
