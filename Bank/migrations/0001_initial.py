# Generated by Django 3.0.4 on 2020-03-17 14:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Citizenship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizenship', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name_plural': 'Citizenship',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60, null=True)),
                ('last_name', models.CharField(max_length=60, null=True)),
                ('otchestvo', models.CharField(max_length=60, null=True)),
                ('birth_date', models.DateField(default=datetime.date.today)),
                ('seria_pasporta', models.CharField(default='MP', max_length=2)),
                ('passport_number', models.IntegerField(null=True, unique=True)),
                ('kem_vidan', models.CharField(max_length=60)),
                ('data_vidachi', models.DateField(default=datetime.date.today)),
                ('ID_number', models.IntegerField(null=True, unique=True)),
                ('birth_place', models.CharField(max_length=60, null=True)),
                ('address_projivaniya', models.CharField(max_length=100, null=True)),
                ('mobile_phone', models.CharField(max_length=20, null=True, unique=True)),
                ('job', models.CharField(max_length=20, null=True, unique=True)),
                ('position', models.CharField(max_length=20, null=True, unique=True)),
                ('address_propiski', models.CharField(max_length=100, null=True)),
                ('family', models.CharField(choices=[('Замужем/Женат', 'Замужем/Женат'), ('Не замужем/Не женат', 'Не замужем/Не женат')], default='Bruh', max_length=9999)),
                ('invalid', models.CharField(choices=[('Нет', 'Нет'), ('1-ая группа', '1-ая группа'), ('2-ая группа', '2-ая группа'), ('3-ая группа', '3-ая группа')], default=1, max_length=9999)),
                ('pensioner', models.BooleanField(default=False, verbose_name='Retired')),
                ('voenoobyazaniy', models.BooleanField(default=False, verbose_name='Army')),
                ('sex', models.BooleanField(choices=[(False, 'Женщина'), (True, 'Мужчина')], default=True, verbose_name='Sex')),
                ('profile_picture', models.ImageField(default='todd.png', upload_to='profile_pictures/')),
                ('citizenship', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Bank.Citizenship')),
                ('city_projivaniya', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='city_projivaniya', to='Bank.City')),
                ('city_propiski', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='city_propiski', to='Bank.City')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
    ]