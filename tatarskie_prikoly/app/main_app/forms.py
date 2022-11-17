from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import TickerData, TransactionHistory

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TradeForm(forms.ModelForm):
    class Meta:
        model = TransactionHistory
        fields = ['buy_currency', 'buy_currency_amount', 'sell_currency', 'sell_currency_amount']
        widgets = {
            'buy_currency': forms.TextInput(attrs={
                'class': 'form-control currency-autocomplete tradeform-predetermined',
                'id': 'tradeform_buy_currency',
            }),
            'buy_currency_amount': forms.NumberInput(attrs={
                'class': 'form-control tradeform-predetermined',
                'id': 'tradeform_buy_amount',
            }),
            'sell_currency': forms.TextInput(attrs={
                'class': 'form-control currency-autocomplete tradeform-predetermined',
                'id': 'tradeform_sell_currency',
            }),
            'sell_currency_amount': forms.NumberInput(attrs={
                'class': 'form-control',
            })

        }

    def clean(self):
        print('UP TO INSTALL BACKEND VALIDATION')
        return self.cleaned_data

class TickerForm(forms.ModelForm):
    class Meta:
        model = TickerData
        fields = '__all__'
        widgets = {
            'currency': forms.TextInput(attrs={'class': 'form-control currency-autocomplete'})
        }

    def clean(self):
        print('UP TO INSTALL BACKEND VALIDATION')
        return self.cleaned_data