from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime, timedelta, tzinfo

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=35, verbose_name='Name')
    desc = models.TextField(max_length=150, verbose_name='Description', blank=True)
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('categories')

    def __str__(self):
        return self.name


# REMINDER_CHOICES = ((1, _('1 day')),
#                     (2, _('3 days')),
#                     (3, _('1 week')),
#                     (4, _('2 weeks')),
#                     (5, _('1 month')),
#                     (6, _('3 months')),
#                     (7, _('6 months')),)


class ReminderChoice(models.Model):
    field = models.CharField(max_length=20)

    def __str__(self):
        return str(self.field)
        # return {'1': '1 day',
        #         '2': '3 days',
        #         '3': '1 week',
        #         '4': '2 weeks',
        #         '5': '1 month',
        #         '6': '3 months',
        #         '7': '6 months'}.get(str(self.field))


class Document(models.Model):
    name = models.CharField(max_length=60, verbose_name='Name')
    desc = models.TextField(max_length=2000, verbose_name='Description', blank=True)
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Category', blank=True, null=True, on_delete=models.SET_NULL)
    expiry_date = models.DateField(verbose_name='Expiry date', blank=True, null=True)
    last_reminder_sent = models.DateTimeField(verbose_name='Last reminder sent', null=True, blank=True, default=None)
    reminder = models.ManyToManyField(ReminderChoice, through='ReminderThrough', blank=True)

    def get_reminders(self):
        reminders = [str(rem.field) for rem in self.reminder.all().order_by('id')]
        if len(reminders) is 0:
            reminders.append("No reminders set")
        return reminders

    def get_last_reminder_sent(self):
        last_reminder_sent = self.last_reminder_sent if self.last_reminder_sent else 'No reminder sent'
        return last_reminder_sent

    def get_absolute_url(self):
        return reverse('docs')

    def __str__(self):
        return self.name


class ReminderThrough(models.Model):
    reminder_choice = models.ForeignKey(ReminderChoice, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.reminder_choice)

    def get_days(self):
        return {'1 day': 1,
                '3 days': 3,
                '1 week': 7,
                '2 weeks': 14,
                '1 month': 30,
                '3 months': 92,
                '6 months': 183}.get(self.reminder_choice.field)

    def get_days_by_id(self):
        return {1: 1,
                2: 3,
                3: 7,
                4: 14,
                5: 30,
                6: 92,
                7: 183}.get(self.reminder_choice.id)


class Announcement(models.Model):
    text = models.TextField(max_length=6000, verbose_name='Text')
