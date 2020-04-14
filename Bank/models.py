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
    first_name = models.CharField(max_length=60, unique=False, null=True)
    last_name = models.CharField(max_length=60, unique=False, null=True)
    otchestvo = models.CharField(max_length=60, unique=False, null=True)
    birth_date = models.DateField(blank=False, default=datetime.date.today)
    sex = models.BooleanField('Sex', choices=SEX_CHOICES, null=False, default=True)
    seria_pasporta = models.CharField(max_length=2, blank=False, null=False, default="MP")

    passport_number = models.IntegerField(unique=True, blank=False, null=True)
    kem_vidan = models.CharField(max_length=60, unique=False, blank=False)
    data_vidachi = models.DateField(blank=False, default=datetime.date.today)
    ID_number = models.IntegerField(unique=True, blank=False, null=True)
    birth_place = models.CharField(max_length=60, unique=False, null=True)
    city_projivaniya = models.ForeignKey('City', on_delete=models.CASCADE, null=False, default=1,
                                         related_name='city_projivaniya')
    address_projivaniya = models.CharField(max_length=100, unique=False, blank=False, null=True)
    mobile_phone = models.CharField(max_length=20, unique=True, blank=False, null=True)
    job = models.CharField(max_length=20, unique=True, blank=False, null=True)
    position = models.CharField(max_length=20, unique=True, blank=False, null=True)
    city_propiski = models.ForeignKey('City', on_delete=models.CASCADE, null=False, default=1,
                                      related_name='city_propiski')
    address_propiski = models.CharField(max_length=100, unique=False, blank=False, null=True)
    citizenship = models.ForeignKey('Citizenship', on_delete=models.CASCADE, null=False, default=1)
    family = models.CharField(max_length=9999, choices=FAMILY_CHOICES, null=False, default="Bruh")

    invalid = models.CharField(max_length=9999, choices=INVALID_CHOICES, null=False, default=1)
    pensioner = models.BooleanField('Retired', null=False, default=False)
    voenoobyazaniy = models.BooleanField('Army', null=False, default=False)

    sex = models.BooleanField('Sex', choices=SEX_CHOICES, null=False, default=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/",
                                        default="todd.png")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)

        if img.height > 450 or img.width > 350:
            new_img = (450, 350)
            img.thumbnail(new_img)
            img.save(self.profile_picture.path)

    def __str__(self):
        return str(self.user.profile.last_name + " " + self.user.profile.first_name)

    class Meta:
        ordering = ['last_name', 'first_name']


class City(models.Model):
    city = models.CharField(max_length=60, unique=False, blank=False)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.city


class Citizenship(models.Model):
    citizenship = models.CharField(max_length=60, unique=False, blank=False)

    class Meta:
        verbose_name_plural = "Citizenship"

    def __str__(self):
        return self.citizenship


class Account(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, unique=False, default=0)

    def __str__(self):
        return str(self.profile.last_name + " " + self.profile.first_name)


class Deposits(models.Model):

    DEPOSIT_TYPE = (
        ("7.5% на 45 дней", "7.5% на 45 дней"),
    )

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    deposit_type = models.CharField(max_length=900, choices=DEPOSIT_TYPE, null=False, default=0)
    deposit_value = models.IntegerField(null=True, blank=False)

    class Meta:
        verbose_name_plural = "Deposits"

    def __str__(self):
        return str(self.profile.last_name + " " + self.profile.first_name)


def create_signal(sender, instance, created, **kwargs):
    if created:
        account = Account.objects.create(profile=instance)
        deposit = Deposits.objects.create(profile=instance)


post_save.connect(create_signal, sender=Profile)
