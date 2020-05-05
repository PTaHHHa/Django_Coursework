from django.db import models
from django.contrib.auth.models import User
import datetime
from PIL import Image
from django.db.models.signals import post_save


# Create your models here.


class Profile(models.Model):
    FAMILY_CHOICES = (
        ("Замужем/Женат", "Замужем/Женат"),
        ("Не замужем/Не женат", "Не замужем/Не женат"),
    )

    INVALID_CHOICES = (
        ("Нет", "Нет"),
        ("1-ая группа", "1-ая группа"),
        ("2-ая группа", "2-ая группа"),
        ("3-ая группа", "3-ая группа"),
    )

    SEX_CHOICES = (
        (False, 'Женщина'),
        (True, 'Мужчина'),
    )

    PENSIONER_CHOICES = (
        (False, 'Нет'),
        (True, 'Да'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60, unique=False, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=60, unique=False, null=True, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=60, unique=False, null=True, verbose_name='Отчество')
    birth_date = models.DateField(blank=False, default=datetime.date.today, verbose_name='Дата рождения')
    passport_series = models.CharField(max_length=2, blank=False, null=False,
                                       default="MP", verbose_name='Серия паспорта')
    passport_number = models.IntegerField(unique=True, blank=False, null=True, verbose_name='Номер паспорта')
    passport_authority = models.CharField(max_length=60, unique=False, blank=False, verbose_name='Кем выдан')
    date_of_issue = models.DateField(blank=False, default=datetime.date.today, verbose_name='Дата выдачи')
    ID_number = models.IntegerField(unique=True, blank=False, null=True, verbose_name='Идентификационный номер')
    birth_place = models.CharField(max_length=60, unique=False, null=True, verbose_name='Место рождения')
    city_of_residence = models.ForeignKey('City', on_delete=models.CASCADE, null=False, default=1,
                                          related_name='city_of_residence', verbose_name='Город проживания')
    address_of_residence = models.CharField(max_length=100, unique=False,
                                            blank=False, null=True, verbose_name='Адрес проживания')
    mobile_phone = models.CharField(max_length=20, unique=True, blank=False, null=True, verbose_name='Моб. тел.')
    job = models.CharField(max_length=20, unique=True, blank=False, null=True, verbose_name='Место работы')
    position = models.CharField(max_length=20, unique=False, blank=False, null=True, verbose_name='Должность')
    citizenship = models.ForeignKey('Citizenship', on_delete=models.CASCADE, null=False, default=1,
                                    verbose_name='Гражданство')
    family_status = models.CharField(max_length=9999, choices=FAMILY_CHOICES, null=False, default="неопределено",
                                     verbose_name='Семейное положение')

    disability = models.CharField('Инвалидность', max_length=9999, choices=INVALID_CHOICES, null=False, default=1)
    pensioner = models.BooleanField('Пенсионер', null=False, default=False)
    military_service = models.BooleanField('Военнообязаный', null=False, default=False)

    sex = models.BooleanField('Пол', choices=SEX_CHOICES, null=False, default=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/",
                                        default="todd.png", verbose_name='Личное фото')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)

        if img.height > 250 or img.width > 200:
            new_img = (250, 200)
            img.thumbnail(new_img)
            img.save(self.profile_picture.path)

    def __str__(self):
        try:
            return str(self.user.profile.last_name + " " + self.user.profile.first_name)
        except TypeError:
            return str(self.user.last_name + " " + self.user.first_name)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'Профили клиентов'


class City(models.Model):
    city = models.CharField(max_length=60, unique=False, blank=False, verbose_name='Город')

    class Meta:
        verbose_name_plural = "Город"

    def __str__(self):
        return self.city


class Citizenship(models.Model):
    citizenship = models.CharField(max_length=60, unique=False, blank=False, verbose_name='Гражданство')

    class Meta:
        verbose_name_plural = "Гражданство"

    def __str__(self):
        return self.citizenship


class Account(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=False, unique=False, default=0,
                                          null=False, verbose_name='Текущий баланс счёта')

    class Meta:
        verbose_name_plural = 'Счета клиентов'

    def __str__(self):
        return str(self.profile.last_name + " " + self.profile.first_name)


class Deposits(models.Model):
    DEPOSIT_TYPE = (
        ("под 11.3% на 95 дней", "под 11.3% на 95 дней"),
        ("под 11.8% на 125 дней", "под 11.8% на 125 дней"),
        ("под 12.8% на 185 дней", "под 12.8% на 185 дней"),
        ("под 13% на 275 дней", "под 13% на 275 дней"),
        ("под 13.2% на 385 дней", "под 13.2% на 385 дней"),
        ("под 12.6% на 550 дней", "под 12.6% на 550 дней"),
        ("под 13% на 735 дней", "под 13% на 735 дней"),
    )

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    deposit_type = models.CharField(max_length=900, choices=DEPOSIT_TYPE, null=False, default=0,
                                    verbose_name='Тип вклада')
    deposit_value = models.IntegerField(blank=False, unique=False, default=0, null=False, verbose_name='Сумма вклада')
    temporary_deposit_income = models.DecimalField(max_digits=10, decimal_places=2,
                                                   blank=False, unique=False, default=0, null=True, editable=False
                                                   , verbose_name='Доход от вклада')
    temporary_total_income = models.DecimalField(max_digits=10, decimal_places=2,
                                                 blank=False, unique=False, default=0, null=True, editable=False
                                                 , verbose_name='Сумма в конце срока')
    deposit_income = models.DecimalField(max_digits=10, decimal_places=2,
                                         blank=False, unique=False, default=0, null=False, editable=False)
    total_income = models.DecimalField(max_digits=10, decimal_places=2,
                                       blank=False, unique=False, default=0, null=False, editable=False)
    deposit_creating_date = models.DateField(blank=False, default=datetime.date.today, editable=False
                                             , verbose_name='Дата открытия вклада')
    deposit_end_date = models.DateField(blank=False, default=datetime.date.today, editable=False,
                                        verbose_name='Дата закрытия вклада')
    tax_rate = models.DecimalField(max_digits=4, decimal_places=2,
                                   blank=False, unique=False, default=0, null=False, editable=False
                                   , verbose_name='Налог')
    percentage = models.DecimalField(max_digits=4, decimal_places=2,
                                     blank=False, unique=False, default=0, null=False, editable=False
                                     , verbose_name='Проценты')
    deposit_days = models.IntegerField(blank=False, unique=False, default=0, null=False, editable=False, verbose_name='Срок вклада в днях')

    def count_deposit_end_date(self):
        if self.deposit_type == Deposits.DEPOSIT_TYPE[0][0]:
            end_date = self.deposit_creating_date + datetime.timedelta(days=95)
            Deposits.objects.update(deposit_end_date=end_date)
            return end_date
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[1][0]:
            end_date = self.deposit_creating_date + datetime.timedelta(days=125)
            Deposits.objects.update(deposit_end_date=end_date)
            return end_date
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[2][0]:
            end_date = self.deposit_creating_date + datetime.timedelta(days=185)
            Deposits.objects.update(deposit_end_date=end_date)
            return end_date
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[3][0]:
            end_date = self.deposit_creating_date + datetime.timedelta(days=275)
            Deposits.objects.update(deposit_end_date=end_date)
            return end_date
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[4][0]:
            end_date = self.deposit_creating_date + datetime.timedelta(days=385)
            Deposits.objects.update(deposit_end_date=end_date)
            return end_date
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[5][0]:
            end_date = self.deposit_creating_date + datetime.timedelta(days=550)
            Deposits.objects.update(deposit_end_date=end_date)
            return end_date
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[6][0]:
            end_date = self.deposit_creating_date + datetime.timedelta(days=735)
            Deposits.objects.update(deposit_end_date=end_date)
            return end_date

    count_deposit_end_date.short_description = "Дата закрытия вклада"
    deposit_end_date_property = property(count_deposit_end_date)

    def count_tax_rate(self):
        if self.deposit_type == Deposits.DEPOSIT_TYPE[0][0] or self.deposit_type == Deposits.DEPOSIT_TYPE[1][0] or self.deposit_type == Deposits.DEPOSIT_TYPE[2][0] or self.deposit_type == Deposits.DEPOSIT_TYPE[3][0]:
            Deposits.objects.update(tax_rate=13)
            return self.tax_rate
        else:
            Deposits.objects.update(tax_rate=0)
            return self.tax_rate

    count_tax_rate.short_description = "Налог"
    tax_rate_property = property(count_tax_rate)

    def count_percentage(self):
        if self.deposit_type == Deposits.DEPOSIT_TYPE[0][0]:
            perc = 11.3
            Deposits.objects.update(percentage=perc)
            return perc
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[1][0]:
            perc = 11.8
            Deposits.objects.update(percentage=perc)
            return perc
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[2][0]:
            perc = 12.8
            Deposits.objects.update(percentage=perc)
            return perc
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[3][0]:
            perc = 13
            Deposits.objects.update(percentage=perc)
            return perc
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[4][0]:
            perc = 13.2
            Deposits.objects.update(percentage=perc)
            return perc
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[5][0]:
            perc = 12.6
            Deposits.objects.update(percentage=perc)
            return perc
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[6][0]:
            perc = 13
            Deposits.objects.update(percentage=perc)
            return perc

    count_percentage.short_description = "Проценты"
    percentage_property = property(count_percentage)

    def count_days(self):
        if self.deposit_type == Deposits.DEPOSIT_TYPE[0][0]:
            days = 95
            Deposits.objects.update(deposit_days=days)
            return days
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[1][0]:
            days = 125
            Deposits.objects.update(deposit_days=days)
            return days
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[2][0]:
            days = 185
            Deposits.objects.update(deposit_days=days)
            return days
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[3][0]:
            days = 275
            Deposits.objects.update(deposit_days=days)
            return days
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[4][0]:
            days = 385
            Deposits.objects.update(deposit_days=days)
            return days
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[5][0]:
            days = 550
            Deposits.objects.update(deposit_days=days)
            return days
        elif self.deposit_type == Deposits.DEPOSIT_TYPE[6][0]:
            days = 735
            Deposits.objects.update(deposit_days=days)
            return days

    count_days.short_description = "Срок вклада в днях"
    days_property = property(count_days)

    def count_total_income(self):
        self.deposit_income_without_tax = self.deposit_value * (self.percentage / 100) * int(self.deposit_days / 365)
        if self.tax_rate != 0:
            self.income_with_tax = self.deposit_income_without_tax * self.tax_rate/100
            total_income = self.deposit_income_without_tax-self.income_with_tax + self.deposit_value
            Deposits.objects.update(temporary_deposit_income=self.income_with_tax, temporary_total_income=total_income)
        else:
            total_income = self.deposit_income_without_tax + self.deposit_value
            Deposits.objects.update(temporary_deposit_income=self.deposit_income_without_tax,
                                    temporary_total_income=total_income)
        if self.deposit_creating_date == self.deposit_end_date:
            Deposits.objects.update(deposit_income=self.deposit_income_without_tax, total_income=total_income,
                                    temporary_deposit_income=None, temporary_total_income=None)
            Account.objects.update(current_balance=(self.deposit_income_without_tax + self.deposit_value))
        return total_income

    count_total_income.short_description = "Сумма в конце срока"
    total_income_property = property(count_total_income)

    class Meta:
        verbose_name_plural = "Вклады"

    def __str__(self):
        return str(self.profile.last_name + " " + self.profile.first_name)


def create_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def create_account_signal(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(profile=instance)
        Deposits.objects.create(profile=instance)


post_save.connect(create_profile_signal, sender=User)
post_save.connect(create_account_signal, sender=Profile)
