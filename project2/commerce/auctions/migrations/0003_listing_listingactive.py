# Generated by Django 3.1.3 on 2020-12-08 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_comments_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='listingActive',
            field=models.BooleanField(default=True),
        ),
    ]
