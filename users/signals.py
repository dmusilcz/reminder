from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from main.models import Category, ReminderChoices


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        for cat_name, cat_desc in (('IDs', 'Default category - IDs'),
                                   ('Car', 'Default category - Car'),
                                   ('Insurance', 'Default category - Insurance')):
            Category.objects.create(name=cat_name, desc=cat_desc, author=instance)


@receiver(post_save, sender=User)
def create_user_reminder_choices(sender, instance, created, **kwargs):
    if created:
        for rem in ('1 day', '3 days', '1 week', '2 weeks', '1 month', '3 months', '6 months'):
            ReminderChoices.objects.create(author=instance, field=rem)
