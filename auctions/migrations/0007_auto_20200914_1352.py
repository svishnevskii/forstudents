# Generated by Django 3.1 on 2020-09-14 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200914_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='listing',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='auctions.listing'),
            preserve_default=False,
        ),
    ]
