# Generated by Django 3.1.3 on 2020-12-11 04:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20201211_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='bidSubmitted',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 11, 4, 4, 34, 596812, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comments',
            name='commentSubmitted',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 11, 4, 4, 34, 597204, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='listingCreated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 11, 4, 4, 34, 596390, tzinfo=utc)),
        ),
    ]