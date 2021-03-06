# Generated by Django 3.0.5 on 2020-04-20 14:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0013_deposits_tax_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deposits',
            old_name='date',
            new_name='deposit_creating_date',
        ),
        migrations.AddField(
            model_name='deposits',
            name='deposit_end_date',
            field=models.DateField(default=datetime.date.today, editable=False),
        ),
    ]
