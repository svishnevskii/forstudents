# Generated by Django 3.1 on 2020-09-11 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20200911_0909'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CategoriesOfRelationship',
            new_name='CategoryListing',
        ),
        migrations.RenameField(
            model_name='watchlist',
            old_name='listing_id',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='watchlist',
            old_name='user_id',
            new_name='user',
        ),
    ]