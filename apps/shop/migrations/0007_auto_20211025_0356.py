# Generated by Django 3.0 on 2021-10-25 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20211024_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='number',
            field=models.CharField(blank=True, db_column='number', help_text='Number', max_length=50, null=True, unique=True, verbose_name='Number'),
        ),
    ]
