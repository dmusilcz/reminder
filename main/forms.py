from django import forms
from users.widgets import FengyuanChenDatePickerInput
from .models import Category, Document, ReminderChoices
from django.utils import timezone
from django.core.exceptions import ValidationError


class DocumentUpdateForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    desc = forms.CharField(required=False)
    category = forms.MultipleChoiceField()
    expiry_date_from = forms.DateField(input_formats=['%m/%d/%Y'], widget=FengyuanChenDatePickerInput(), required=False, initial=timezone.localdate(timezone.now()))
    expiry_date_to = forms.DateField(input_formats=['%m/%d/%Y'], widget=FengyuanChenDatePickerInput(), required=False)
    reminder = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SearchForm, self).__init__(*args, **kwargs)
        reminders = ReminderChoices.objects.filter(author=self.request.user).order_by('id')
        reminder_names = ['1 day', '3 days', '1 week', '2 weeks', '1 month', '3 months', '6 months']
        reminder_ids = [choice.id for choice in reminders]
        reminder_names.insert(0, 'No reminder set')
        reminder_ids.insert(0, '0')
        self.fields['reminder'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=((id, time) for id, time in zip(reminder_ids, reminder_names)))
        categories = Category.objects.filter(author=self.request.user).order_by('name')
        category_names = [category.name for category in categories]
        category_ids = [category.id for category in categories]
        category_names.insert(0, 'No category set')
        category_ids.insert(0, '0')
        self.fields['category'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                                            choices=((id, category) for id, category in zip(category_ids, category_names)))

    def clean(self):
        cd = self.cleaned_data

        expiry_date_from = cd.get("expiry_date_from")
        expiry_date_to = cd.get("expiry_date_to")

        if expiry_date_from and expiry_date_to and expiry_date_from > expiry_date_to:
            # Or you might want to tie this validation to the password1 field
            raise ValidationError("Entered 'Expiry date from' is later than 'Expiry date to'")

        return cd