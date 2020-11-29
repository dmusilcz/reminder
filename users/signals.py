from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from main.models import Category
from django.utils.translation import gettext_lazy as _


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        for cat_name in (_('IDs'), _('Car'), _('Insurance')):
            Category.objects.create(name=cat_name, author=instance)
