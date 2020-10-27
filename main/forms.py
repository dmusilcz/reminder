from django import forms
from users.widgets import FengyuanChenDatePickerInput
from .models import Category, Document, ReminderChoices
from django.utils import timezone
from django.core.exceptions import ValidationError


class DocumentUpdateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'desc', 'category', 'expiry_date', 'reminder']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(DocumentUpdateForm, self).__init__(*args, **kwargs)
        # ids = [choice.id for choice in ReminderChoices.objects.filter(author=self.request.user).order_by('id')]
        self.fields['category'].queryset = Category.objects.filter(author=self.request.user)
        self.fields['expiry_date'] = forms.DateField(input_formats=['%m/%d/%Y'], widget=FengyuanChenDatePickerInput(
                                                     attrs={'oninput': "verifyDate()",
                                                            'onshow': "verifyDate()",
                                                            'autocomplete': 'off'}
        ),
                                                     required=False,
                                                     help_text='Reminders can be chosen once this field is not empty')
        self.fields['reminder'].widget = forms.CheckboxSelectMultiple()
        self.fields['reminder'].queryset = ReminderChoices.objects.filter(author=self.request.user).order_by('id')


class SearchForm(forms.Form):
    name = forms.CharField(required=False, label='<b>Name</b> contains:')
    desc = forms.CharField(required=False, label='<b> Description</b> contains:')
    category = forms.MultipleChoiceField()
    expiry_date_from = forms.DateField(input_formats=['%m/%d/%Y'], widget=FengyuanChenDatePickerInput(), required=False, label='<b>Expiry date</b> from:')
    expiry_date_to = forms.DateField(input_formats=['%m/%d/%Y'], widget=FengyuanChenDatePickerInput(), required=False, label='<b>Expiry date</b> to:', help_text="Tip: you can search for expired documents by only setting the <i><b>Expiry date</b> to</i>.")
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
                                                            choices=((id, category) for id, category in zip(category_ids, category_names)), label='<b>Category</b>:')

    def clean(self):
        cd = self.cleaned_data

        expiry_date_from = cd.get("expiry_date_from")
        expiry_date_to = cd.get("expiry_date_to")

        if expiry_date_from and expiry_date_to and expiry_date_from > expiry_date_to:
            # Or you might want to tie this validation to the password1 field
            raise ValidationError("Entered 'Expiry date from' is later than 'Expiry date to'")

        return cd