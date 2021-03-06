# Generated by Django 3.1.3 on 2020-12-11 08:26

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auto_20201211_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='bidSubmitted',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 11, 8, 26, 15, 132243, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comments',
            name='commentSubmitted',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 11, 8, 26, 15, 132645, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='listingCreated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 11, 8, 26, 15, 131349, tzinfo=utc)),
        ),
        migrations.RemoveField(
            model_name='listing',
            name='listingWinner',
        ),
        migrations.AddField(
            model_name='listing',
            name='listingWinner',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
