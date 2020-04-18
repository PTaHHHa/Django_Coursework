from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from Bank.models import Profile, Deposits, Account
from Bank.forms import ProfileForm, ImageForm, DepositForm, AccountForm
from datetime import datetime, date

# Create your views here.
global deposit_creating_time, percentage


def index(request):
    return render(request, "../templates/base.html")


def update_profile(request):
    if request.user.is_authenticated:
        try:
            p = request.user
            form = ProfileForm(request.POST or None, instance=p.profile)
            image = ImageForm(request.POST, request.FILES, instance=p.profile)
        except Profile.DoesNotExist:
            p = Profile(user=request.user)
            form = ProfileForm(request.POST or None, instance=p)
            image = ImageForm(request.POST, request.FILES, instance=p)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                image.save()
                messages.success(request, f'Your account has been updated')
                return redirect('profile')
    else:
        messages.error(request, 'You should login first')
        return redirect('index')
    return render(request, "../templates/update_profile.html", {'form': form})


@login_required
def user_profile(request):
    deposit_counter(request)
    return render(request, "../templates/profile.html")


def delete_profile(request):
    b = Profile.objects.get(user=request.user)
    b.delete()
    logout(request)
    messages.success(request, 'Account was successfully deleted')
    return render(request, '../templates/base.html')


def account_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            p = request.user.profile
            account = AccountForm(request.POST, instance=p.account)
            if account.is_valid():
                account.save()
                return redirect('profile')
        else:
            account = AccountForm()
            return render(request, "../templates/account_profile.html", {'account': account})
    else:
        messages.error(request, 'You should login first')
        return redirect('index')


def deposit(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            p = request.user.profile
            deposit_form = DepositForm(request.POST, instance=p.deposits)

            if deposit_form.is_valid():
                account_object = Account.objects.get(id=p.account.id)
                account_value_object = getattr(account_object, 'current_balance')
                deposit_value_object = deposit_form.cleaned_data['deposit_value']
                if deposit_value_object < 100:
                    messages.error(request, 'Minimal deposit value 100 руб.')
                    return redirect('profile')
                elif deposit_value_object > account_value_object:
                    messages.error(request, "You don't have enough money to make a deposit!")
                    return redirect('profile')
                else:
                    deposit_form.save()
                    account_object.current_balance = account_value_object - deposit_value_object
                    account_object.save()

                    messages.success(request, 'Deposit created')

                    """ПРОРАБОТАТЬ ФУНКЦИОНАЛ ДЛЯ ДАТЫ В deposit_counter()"""
                    deposit_creating_time = date.today()
                    Deposits.objects.update(date=deposit_creating_time)
                    print(deposit_creating_time)

                    return redirect('profile')
        else:
            deposit_form = DepositForm()
            return render(request, "../templates/deposit_form.html", {'deposit_form': deposit_form})
    else:
        messages.error(request, 'You should login first')
        return redirect('index')


"""ПЕРЕДЕЛАТЬ ФОРМУЛЫ"""


def deposit_counter(request):
    tax = 13
    deposit_object = Deposits.objects.get(id=request.user.profile.deposits.id)
    deposit_value_object = getattr(deposit_object, 'deposit_value')
    deposit_type_object = getattr(deposit_object, 'deposit_type')
    if deposit_type_object == Deposits.DEPOSIT_TYPE[0][0]:
        percentage = 0.11
        days = 45
        deposit_income = deposit_value_object * percentage * (tax / 100)
        print(deposit_value_object * percentage)
        Deposits.objects.update(deposit_income=deposit_income, tax_rate=13,
                                total_income=(deposit_income + deposit_value_object))
    elif deposit_type_object == Deposits.DEPOSIT_TYPE[1][0]:
        percentage = 0.113
        days = 95
        deposit_income = deposit_value_object * percentage * (tax / 100)
        Deposits.objects.update(deposit_income=deposit_income, tax_rate=13,
                                total_income=(deposit_income + deposit_value_object))
    elif deposit_type_object == Deposits.DEPOSIT_TYPE[2][0]:
        percentage = 0.128
        days = 185
        deposit_income = deposit_value_object * percentage * (tax / 100)
        Deposits.objects.update(deposit_income=deposit_income, tax_rate=13,
                                total_income=(deposit_income + deposit_value_object))
    elif deposit_type_object == Deposits.DEPOSIT_TYPE[3][0]:
        percentage = 0.132
        days = 385
        tax = 0
        deposit_income = deposit_value_object * percentage
        Deposits.objects.update(deposit_income=deposit_income, tax_rate=tax,
                                total_income=(deposit_income + deposit_value_object))
    elif deposit_type_object == Deposits.DEPOSIT_TYPE[4][0]:
        percentage = 0.125
        days = 735
        tax = 0
        deposit_income = deposit_value_object * percentage
        Deposits.objects.update(deposit_income=deposit_income, tax_rate=tax,
                                total_income=(deposit_income + deposit_value_object))
