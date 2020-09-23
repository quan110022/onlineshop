from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

Payment_choise = {

    ('M', 'MoMo'),
    ('T', 'Timo'),
}

class CheckoutForm(forms.Form):
    address = forms.CharField()
    country = CountryField(blank_label='(select country)').formfield(
            attrs={
                'class': 'custom-select d-block w-100'}
    )
    zip = forms.CharField()

    save = forms.BooleanField(widget=forms.CheckboxInput())
    payment = forms.ChoiceField(
        widget=forms.RadioSelect, choices=Payment_choise)
