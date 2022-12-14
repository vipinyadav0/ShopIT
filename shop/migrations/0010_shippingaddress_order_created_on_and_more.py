# Generated by Django 4.1.1 on 2022-11-27 10:34

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_order_price_order_quantity_delete_customerdetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'ShippingAddress',
                'verbose_name_plural': 'ShippingAddresss',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 11, 27, 10, 34, 6, 693038, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_payment_intent',
            field=models.CharField(default=datetime.datetime(2022, 11, 27, 10, 34, 40, 176242, tzinfo=datetime.timezone.utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='updated_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
