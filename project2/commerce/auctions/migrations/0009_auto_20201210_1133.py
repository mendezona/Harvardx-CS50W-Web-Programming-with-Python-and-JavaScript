# Generated by Django 3.1.3 on 2020-12-10 00:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20201209_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='bidSubmitted',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 10, 0, 33, 27, 157209, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comments',
            name='commentSubmitted',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 10, 0, 33, 27, 157606, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='listingCreated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 10, 0, 33, 27, 156780, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watchlistListingID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
                ('watchlistUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]