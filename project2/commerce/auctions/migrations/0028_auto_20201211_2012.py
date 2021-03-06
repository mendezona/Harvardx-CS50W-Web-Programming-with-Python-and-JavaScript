# Generated by Django 3.1.3 on 2020-12-11 09:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_auto_20201211_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='bidSubmitted',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 11, 9, 12, 41, 727940, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comments',
            name='commentSubmitted',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 11, 9, 12, 41, 728325, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='listingCreated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 11, 9, 12, 41, 727511, tzinfo=utc)),
        ),
    ]
