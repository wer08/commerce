# Generated by Django 4.1.1 on 2022-09-19 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(blank=True, choices=[('Clothing', 'Clothing'), ('Car', 'Car'), ('RTV', 'RTV'), ('AGD', 'AGD'), ('Toy', 'Toy'), ('Home', 'Home')], max_length=10),
        ),
    ]
