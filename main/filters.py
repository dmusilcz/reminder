from .models import Category, Document, ReminderChoices
from django import forms
import django_filters


def categories(request):
    if request is None:
        return Category.objects.none()

    # return Category.objects.filter(author=request.user)
    return request.user.category_set.all()

def reminders(request):
    if request is None:
        return ReminderChoices.objects.none()

    return ReminderChoices.objects.filter(author=request.user).order_by('id')


# class DocFilter(django_filters.FilterSet):
#     category = django_filters.ModelMultipleChoiceFilter(queryset=categories,
#                                                 widget=forms.CheckboxSelectMultiple,
#                                                 help_text='If no category is selected, all results will be included - with or without category. If any category is selected, results with no category are excluded.')
#     reminder = django_filters.ModelMultipleChoiceFilter(queryset=reminders, widget=forms.CheckboxSelectMultiple)
#
#     class Meta:
#         model = Document
#         fields = ['name', 'desc', 'category', 'expiry_date', 'reminder', ]
