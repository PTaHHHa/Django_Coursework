# Generated by Django 3.0.5 on 2020-04-15 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0006_auto_20200415_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposits',
            name='deposit_type',
            field=models.CharField(choices=[('Нет', 'Нет'), ('под 7.5% на 45 дней', 'под 7.5% на 45 дней')], default=1, max_length=900),
        ),
    ]
