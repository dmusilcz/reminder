from django.forms import DateInput


class FengyuanChenDatePickerInput(DateInput):
    template_name = 'users/widgets/fengyuanchen_datepicker.html'