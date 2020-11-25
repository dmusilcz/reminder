from django.contrib import admin

# Register your models here.

from .models import Category, Document, ReminderChoice, ReminderThrough, Announcement

admin.site.register(Category)
admin.site.register(Document)
admin.site.register(ReminderChoice)
admin.site.register(ReminderThrough)
admin.site.register(Announcement)

