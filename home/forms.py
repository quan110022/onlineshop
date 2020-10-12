from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import check_out
Payment_choise = {
    ('S', 'stripe'),
    ('P', 'paypal'),
}

class CheckoutForm(forms.Form):
    address = forms.CharField()
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget()
    )
    zip = forms.CharField()
    save_info = forms.BooleanField(required=False)
    payment = forms.ChoiceField(
        widget=forms.RadioSelect, choices=Payment_choise)
