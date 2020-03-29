from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField

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


REMINDER_CHOICES = ((1, '1 day'),
                    (2, '3 days'),
                    (3, '1 week'),
                    (4, '2 weeks'),
                    (5, '1 month'),
                    (6, '3 months'),
                    (7, '6 months'))


class ReminderChoices(models.Model):
    field = models.CharField(max_length=7, choices=REMINDER_CHOICES)


class Document(models.Model):
    name = models.CharField(max_length=60, verbose_name='Name')
    desc = models.TextField(max_length=200, verbose_name='Description', blank=True)
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Category', blank=True, null=True, on_delete=models.CASCADE)
    expiry_date = models.DateField(verbose_name='Expiry date', blank=True, null=True)
    #reminder = MultiSelectField(choices=REMINDER_CHOICES, default=REMINDER_CHOICES[0])
    reminder = models.ManyToManyField(ReminderChoices)

    def get_reminders(self):
        return ', '.join([rem.field for rem in self.reminder.all()])

    def get_absolute_url(self):
        return reverse('docs')

    def __str__(self):
        return self.name
