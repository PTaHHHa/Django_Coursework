# Generated by Django 3.0.5 on 2020-04-21 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0015_auto_20200420_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposits',
            name='deposit_type',
            field=models.CharField(choices=[('под 11% на 35 дней', 'под 11% на 35 дней'), ('под 12.5% на 95 дней', 'под 12.5% на 95 дней'), ('под 12% на 185 дней', 'под 12% на 185 дней'), ('под 12.1% на 275 дней', 'под 12.1% на 275 дней'), ('под 12.5% на 370 дней', 'под 12.5% на 370 дней'), ('под 12.5% на 735 дней', 'под 12.5% на 735 дней'), ('под 11% на 37 месяцев', 'под 11% на 37 месяцев')], default=0, max_length=900),
        ),
    ]