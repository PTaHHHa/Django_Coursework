# Generated by Django 3.0.5 on 2020-05-05 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0027_auto_20200505_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposits',
            name='tax_rate',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=4, verbose_name='Налог'),
        ),
    ]