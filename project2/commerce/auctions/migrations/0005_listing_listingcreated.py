# Generated by Django 3.1.3 on 2020-12-09 01:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20201208_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='listingCreated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]