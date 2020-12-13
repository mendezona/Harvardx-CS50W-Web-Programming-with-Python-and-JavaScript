# Generated by Django 3.1.3 on 2020-12-09 06:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201209_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='listingCreated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 9, 6, 40, 34, 925963, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='listingPrice',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]