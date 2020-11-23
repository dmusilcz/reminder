from django.contrib import admin
from django.contrib.sites.models import Site

# Register your models here.

from .models import Category, Document, ReminderChoice, ReminderThrough, Announcement

admin.site.register(Category)
admin.site.register(Document)
admin.site.register(ReminderChoice)
admin.site.register(ReminderThrough)
admin.site.register(Announcement)
# admin.site.register(Site)

