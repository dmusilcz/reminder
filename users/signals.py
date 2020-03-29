from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from main.models import Category


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        for cat_name, cat_desc in (('IDs', 'Default category - IDs'),
                                   ('Car', 'Default category - Car'),
                                   ('Insurance', 'Default category - Insurance')):
            Category.objects.create(name=cat_name, desc=cat_desc, author=instance)

