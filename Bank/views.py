from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from Bank.models import Profile, Deposits, Account
from Bank.forms import ProfileForm, ImageForm, DepositForm, AccountForm
from datetime import timedelta, date


# Create your views here.


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
                messages.success(request, f'Информация была обновлена')
                return redirect('profile')
    else:
        messages.error(request, 'Необходимо войти в аккаунт')
        return redirect('index')
    return render(request, "../templates/update_profile.html", {'form': form})


@login_required
def user_profile(request):
    try:
        deposit_billing(request)
    except Profile.DoesNotExist:
        return render(request, "../templates/profile.html")
    finally:
        return render(request, "../templates/profile.html")


def delete_profile(request):
    b = Profile.objects.get(user=request.user)
    b.delete()
    logout(request)
    messages.success(request, 'Аккаунт удалён успешно')
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
        messages.error(request, 'Необходимо войти в аккаунт')
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
                    messages.error(request, 'Минимальная сумма вклада 100 руб.')
                    return redirect('profile')
                elif deposit_value_object > account_value_object:
                    messages.error(request, "Недостаточно средств!")
                    return redirect('profile')
                else:
                    deposit_form.save()
                    account_object.current_balance = account_value_object - deposit_value_object
                    account_object.save()

                    messages.success(request, 'Вклад открыт!')

                    deposit_creating_time = date.today()
                    Deposits.objects.update(deposit_creating_date=deposit_creating_time)

                    deposit_object = Deposits.objects.get(id=request.user.profile.deposits.id)
                    deposit_type_object = getattr(deposit_object, 'deposit_type')
                    if deposit_type_object == Deposits.DEPOSIT_TYPE[0][0]:
                        Deposits.objects.filter(profile=request.user.profile) \
                            .update(deposit_end_date=(deposit_creating_time + timedelta(days=95)))
                    elif deposit_type_object == Deposits.DEPOSIT_TYPE[1][0]:
                        Deposits.objects.filter(profile=request.user.profile) \
                            .update(deposit_end_date=(deposit_creating_time + timedelta(days=125)))
                    elif deposit_type_object == Deposits.DEPOSIT_TYPE[2][0]:
                        Deposits.objects.filter(profile=request.user.profile) \
                            .update(deposit_end_date=(deposit_creating_time + timedelta(days=185)))
                    elif deposit_type_object == Deposits.DEPOSIT_TYPE[3][0]:
                        Deposits.objects.filter(profile=request.user.profile) \
                            .update(deposit_end_date=(deposit_creating_time + timedelta(days=275)))
                    elif deposit_type_object == Deposits.DEPOSIT_TYPE[4][0]:
                        Deposits.objects.filter(profile=request.user.profile) \
                            .update(deposit_end_date=(deposit_creating_time + timedelta(days=385)))
                    elif deposit_type_object == Deposits.DEPOSIT_TYPE[5][0]:
                        Deposits.objects.filter(profile=request.user.profile) \
                            .update(deposit_end_date=(deposit_creating_time + timedelta(days=550)))
                    elif deposit_type_object == Deposits.DEPOSIT_TYPE[6][0]:
                        Deposits.objects.filter(profile=request.user.profile) \
                            .update(deposit_end_date=(deposit_creating_time + timedelta(days=735)))

                    return redirect('profile')
        else:
            deposit_form = DepositForm()
            return render(request, "../templates/deposit_form.html", {'deposit_form': deposit_form})
    else:
        messages.error(request, 'Необходимо войти в аккаунт')
        return redirect('index')


def deposit_counter(request, percentage, tax, days):
    deposit_object = Deposits.objects.get(id=request.user.profile.deposits.id)
    deposit_value_object = getattr(deposit_object, 'deposit_value')
    deposit_creating_date = getattr(deposit_object, 'deposit_creating_date')
    deposit_end_date = getattr(deposit_object, 'deposit_end_date')
    deposit_income_without_tax = deposit_value_object * (percentage/100)*(days/365)
    if tax != 0:
        tax_rate = deposit_income_without_tax * tax/100
        Deposits.objects.filter(profile=request.user.profile) \
            .update(tax_rate=tax_rate)
        total_income = deposit_income_without_tax - tax_rate+deposit_value_object
    else:
        total_income = deposit_income_without_tax+deposit_value_object
        Deposits.objects.filter(profile=request.user.profile) \
            .update(tax_rate=0)
    Deposits.objects.filter(profile=request.user.profile).update(temporary_deposit_income=deposit_income_without_tax,
                                                                 temporary_total_income=total_income)
    if deposit_creating_date == deposit_end_date:
        Deposits.objects.filter(profile=request.user.profile).update(deposit_income=deposit_income_without_tax,
                                                                     total_income=total_income,
                                                                     temporary_deposit_income=None,
                                                                     temporary_total_income=None)
        Account.objects.update(current_balance=(deposit_income_without_tax + deposit_value_object))


def deposit_billing(request):
    deposit_object = Deposits.objects.get(id=request.user.profile.deposits.id)
    deposit_type_object = getattr(deposit_object, 'deposit_type')
    if deposit_type_object == Deposits.DEPOSIT_TYPE[0][0]:
        days = 95
        tax = 13
        percentage = 11.3
        deposit_counter(request, percentage, tax, days)
    elif deposit_type_object == Deposits.DEPOSIT_TYPE[1][0]:
        days = 125
        tax = 13
        percentage = 11.8
        deposit_counter(request, percentage, tax, days)
    elif deposit_type_object == Deposits.DEPOSIT_TYPE[2][0]:
        days = 185
        tax = 13
        percentage = 12.8
        deposit_counter(request, percentage, tax, days)
    elif deposit_type_object == Deposits.DEPOSIT_TYPE[3][0]:
        days = 275
        tax = 13
        percentage = 13
        deposit_counter(request, percentage, tax, days)
    elif deposit_type_object == Deposits.DEPOSIT_TYPE[4][0]:
        days = 385
        percentage = 13.2
        deposit_counter(request, percentage, tax=0, days=days)
    elif deposit_type_object == Deposits.DEPOSIT_TYPE[5][0]:
        days = 550
        percentage = 12.6
        deposit_counter(request, percentage, tax=0, days=days)
    elif deposit_type_object == Deposits.DEPOSIT_TYPE[6][0]:
        days = 735
        percentage = 13
        deposit_counter(request, percentage, tax=0, days=days)
