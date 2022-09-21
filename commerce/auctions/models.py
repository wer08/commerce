from urllib import request
from django.contrib.auth.models import AbstractUser
from django.db import models
from crum import get_current_user




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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=10240,default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqEWgS0uxxEYJ0PsOb2OgwyWvC0Gjp8NUdPw&usqp=CAU",blank=True,null=True)

    def __str__(self):
        return f"Title: {self.title}, decription: {self.description}, current price: {self.current_price}"
    
    def save(self, *args, **kwargs):
        if self.current_price == None:
            self.current_price = self.starting_bid
        self.owner = get_current_user()
        super().save(*args, **kwargs)

class Bid(models.Model):
    listing_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):    
        self.bidder = get_current_user()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.bidder} bid : {self.bid} on : {self.listing_id}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)




    

