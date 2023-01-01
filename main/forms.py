from django import forms
from users.widgets import FengyuanChenDatePickerInput
from .models import Category, Document, ReminderChoice
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from antispam.honeypot.forms import HoneypotField


class DocumentUpdateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'desc', 'category', 'expiry_date', 'reminder']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(DocumentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=self.request.user)
        self.fields['category'].label = _('Category')
        self.fields['expiry_date'] = forms.DateField(required=False,
                                                     help_text=_('Reminders can be chosen once this field is not empty'),
                                                     label=_('Expiry date'))
        self.fields['expiry_date'].widget.attrs = {'oninput': "verifyDate()",
                                                   'autocomplete': 'off'}
        self.fields['reminder'].widget = forms.CheckboxSelectMultiple()
        self.fields['reminder'].queryset = ReminderChoice.objects.all().order_by('id')
        self.fields['reminder'].label = _('Email reminders before expiration')
        self.fields['name'].label = _('Name')
        self.fields['desc'].label = _('Description')


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'desc']

    def __init__(self, *args, **kwargs):
        super(CategoryUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = _('Name')
        self.fields['desc'].label = _('Description')


class SearchForm(forms.Form):
    name = forms.CharField(required=False, label=_('<b>Name</b> contains:'))
    desc = forms.CharField(required=False, label=_('<b>Description</b> contains:'))
    category = forms.MultipleChoiceField()
    expiry_date_from = forms.DateField(
        # input_formats=['%m/%d/%Y'],
        widget=FengyuanChenDatePickerInput(), required=False, label=_('<b>Expiry date</b> from:'))
    expiry_date_to = forms.DateField(
        # input_formats=['%m/%d/%Y'],
        widget=FengyuanChenDatePickerInput(), required=False, label=_('<b>Expiry date</b> to:'))
    reminder = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SearchForm, self).__init__(*args, **kwargs)
        reminders = ReminderChoice.objects.all().order_by('id')
        reminder_names = [choice.field for choice in reminders]
        reminder_ids = [choice.id for choice in reminders]
        reminder_names.insert(0, _('No reminder set'))
        reminder_ids.insert(0, '0')
        self.fields['reminder'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=((id, time) for id, time in zip(reminder_ids, reminder_names)))
        categories = Category.objects.filter(author=self.request.user).order_by('name')
        category_names = [category.name for category in categories]
        category_ids = [category.id for category in categories]
        category_names.insert(0, _('No category set'))
        category_ids.insert(0, '0')
        self.fields['category'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                                            choices=((id, category) for id, category in zip(category_ids, category_names)), label=_('<b>Category</b>:'))
        self.fields['reminder'].label = _('Email reminders before expiration:')

    def clean(self):
        cd = self.cleaned_data

        expiry_date_from = cd.get("expiry_date_from")
        expiry_date_to = cd.get("expiry_date_to")

        if expiry_date_from and expiry_date_to and expiry_date_from > expiry_date_to:
            raise ValidationError(_("Entered 'Expiry date from' is later than 'Expiry date to'"))

        return cd


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True, label=_("Email"))
    subject = forms.CharField(max_length=200, required=False, label=_("Subject"))
    message = forms.CharField(max_length=10000, required=True, label=_("Message"), widget=forms.Textarea())
    name = HoneypotField()
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ContactForm, self).__init__(*args, **kwargs)

        if self.request.user.is_authenticated:
            self.fields['email'].initial = self.request.user.email
