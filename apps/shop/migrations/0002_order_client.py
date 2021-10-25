# Generated by Django 3.0 on 2021-10-20 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(db_column='client_id', help_text='Client', on_delete=django.db.models.deletion.CASCADE, related_name='shop_order', related_query_name='shop_orders', to=settings.AUTH_USER_MODEL, verbose_name='Client'),
        ),
    ]
