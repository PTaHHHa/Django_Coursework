# Generated by Django 3.0.5 on 2020-05-05 10:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0024_auto_20200427_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposits',
            name='deposit_end_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата закрытия вклада'),
        ),
        migrations.AlterField(
            model_name='deposits',
            name='tax_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Налог'),
        ),
    ]
