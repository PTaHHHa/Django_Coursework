import datetime
from datetime import date

from django.contrib import admin
from Bank.models import Profile, Deposits, Account
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)


class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    prepopulated_fields = {'username': ('first_name', 'last_name',)}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2',),
        }),
    )


class DateInput(forms.DateInput):
    input_type = 'date'


class BasicForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {'birth_date': DateInput, 'data_vidachi': DateInput, 'sex': forms.RadioSelect,
                   'passport_series': forms.TextInput(attrs={'pattern': '[a-zA-Zа-яА-Я]+', 'style': 'max-width: 12em'}),
                   'first_name': forms.TextInput(attrs={'pattern': '[-a-zA-Zа-яА-Я]+'}),
                   'last_name': forms.TextInput(attrs={'pattern': '[-a-zA-Zа-яА-Я]+'}),
                   'middle_name': forms.TextInput(attrs={'pattern': '[-a-zA-Zа-яА-Я]+'}),
                   'passport_authority': forms.TextInput(attrs={'pattern': '[-a-zA-Zа-яА-Я]+'}),
                   'birth_place': forms.TextInput(attrs={'pattern': '[-a-zA-Zа-яА-Я]+'}),
                   'address': forms.TextInput(attrs={'pattern': '[-0-9a-zA-Zа-яА-Я]+'}),
                   'mobile_phone': forms.TextInput(attrs={'pattern':
                                                              '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'}),
                   'pensioner': forms.CheckboxInput,
                   'military_service': forms.CheckboxInput,
                   'job': forms.TextInput(attrs={'pattern': '[ -0-9a-zA-Zа-яА-Я]+'}),
                   'position': forms.TextInput(attrs={'pattern': '[ -0-9a-zA-Zа-яА-Я]+'}), }
        fields = '__all__'


class ImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', ]


class ProfileForm(forms.ModelForm):
    form = BasicForm

    class Meta:
        model = Profile
        exclude = ['user']


class ProfileAdmin(admin.ModelAdmin):
    form = BasicForm


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['profile']


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposits
        fields = '__all__'
        exclude = ['profile']
        widgets = {'deposit_type': forms.RadioSelect}


class AccountAdmin(admin.ModelAdmin):
    form = AccountForm


class DepositAdmin(admin.ModelAdmin):
    readonly_fields = ('temporary_deposit_income', 'total_income_property', 'tax_rate_property',
                       'deposit_creating_date', 'deposit_end_date_property', 'percentage_property', 'days_property',)
    form = DepositForm

