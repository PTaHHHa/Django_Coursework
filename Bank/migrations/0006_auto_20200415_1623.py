# Generated by Django 3.0.5 on 2020-04-15 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0005_auto_20200415_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposits',
            name='deposit_type',
            field=models.CharField(choices=[('7.5% на 45 дней', '7.5% на 45 дней')], default='fuck', max_length=900),
        ),
    ]