# Generated by Django 4.1.1 on 2022-09-20 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.CharField(blank=True, default='No image', max_length=1024, null=True),
        ),
    ]