# Generated by Django 3.1.3 on 2020-12-08 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_listingactive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='listingImage',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
