from tokenize import Token
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):

    categories = [
    ("Clothing","Clothing"),
    ("Car","Car"),
    ("RTV","RTV"),
    ("AGD","AGD"),
    ("Toy","Toy"),
    ("Home","Home")
    ]

    title = models.CharField(max_length=64)
    category = models.CharField(max_length=10, blank=True, choices=categories)
    description = models.CharField(max_length=512)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200,default="No image",blank=True,null=True)

    def __str__(self):
        return f"Title: {self.title}, decription: {self.description}, current price: {self.current_price}"
    
    def save(self, *args, **kwargs):
        self.current_price = self.starting_bid
        super().save(*args, **kwargs)

class Bids(models.Model):
    listing_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid = models.IntegerField()

    

