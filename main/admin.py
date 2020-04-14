from django.contrib import admin

# Register your models here.

from .models import Category, Document, ReminderChoices, ReminderThrough

admin.site.register(Category)
admin.site.register(Document)
