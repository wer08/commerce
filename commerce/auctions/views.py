from re import search
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from decimal import Decimal
from .models import User, AuctionListing, Watchlist, Comment, Bid
from operator import itemgetter
from django.contrib import messages
from .functions import checkWatchlist, getComments, getWinner, searchedList


class SearchingForm(forms.Form):
    search = forms.CharField()

class NewListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "category", "description", "starting_bid", "image"]

class NewBidForm(forms.Form):
    bid = forms.DecimalField() 

class NewCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label="")


def newListing(request):
    if request.method == "POST":
        f = NewListingForm(request.POST)
        f.save()
        return redirect("index")

    return render(request, "auctions/newListing.html",{
        "form": NewListingForm()
    })

def categories(request):
    categories = map(itemgetter(0), AuctionListing.categories)
    return render(request, "auctions/categories.html",{
        "categories": categories
    })

def category_listing(request, category_listing):
    list_of_objects = AuctionListing.objects.filter(category=category_listing)
    return render(request, "auctions/category_listing.html",{
        "category_listing": category_listing,
        "list": list_of_objects
    })
def watchlist(request):
    listings = []
    list = Watchlist.objects.filter(user = request.user.id)
    for object in list:
        listings.append(object.listing)

    return render(request, "auctions/watchlist.html",{
        "listings": listings
    })

def addWatchlist(request,listing):
    listing_object = AuctionListing.objects.get(pk = listing)
    if checkWatchlist(request,listing_object):
        new_object = Watchlist.objects.get(listing = listing_object, user = request.user)
        new_object.delete()
        return redirect("index")
    else:
        new_object = Watchlist(listing = listing_object, user = request.user)
        new_object.save()
        return redirect("listing",listing)


def addComment(request):
    if request.method == "POST":
        form2 = NewCommentForm(request.POST)
        listing = request.POST["listing"]
        listing_object = AuctionListing.objects.get(id = int(listing))
        if form2.is_valid():
            print("I'm here")
            comment = form2.cleaned_data["comment"]
            comment_object = Comment(comment = comment, listing = listing_object, user = request.user)
            comment_object.save()
    return redirect("listing",listing)

def closeAuction(request,listing):
    listing_object = AuctionListing.objects.get(pk = listing)
    if request.method == "POST":
        if request.user == listing_object.owner:
            listing_object.active = False
            listing_object.save()
            winner = getWinner(listing_object)
            messages.add_message(request, messages.SUCCESS, f'You succesfully closed the auction, winner is {winner}')
            return redirect("listing",listing)
            

def listing(request, listing):

    listing_object = AuctionListing.objects.get(pk = listing)
    comments = getComments(listing_object)
    
    if request.method == "POST":
        
        listing_object = AuctionListing.objects.get(pk = listing)
        form = NewBidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['bid']
            if bid > listing_object.current_price:
                bid_object = Bid(bid = bid, listing_id = listing_object)
                bid_object.save()
                new_price = bid_object.bid
                listing_object.current_price = new_price
                listing_object.save()
                messages.add_message(request, messages.SUCCESS, 'Your bid was succesful')
                return redirect("index")
            else:
                messages.add_message(request, messages.WARNING, 'Bid must be higher than current price')
                return render(request, "auctions/listing.html", {
                    "flag": checkWatchlist(request,listing_object),
                    "listing": listing_object,
                    "form": NewBidForm(initial={"bid": listing_object.current_price + round(Decimal(0.10),2)}),
                    "form2": NewCommentForm(),
                    "comments": comments,
                })

    return render(request, "auctions/listing.html", {
        "flag": checkWatchlist(request,listing_object),
        "listing": listing_object,
        "form": NewBidForm(initial={"bid": listing_object.current_price + round(Decimal(0.10),2)}),
        "form2": NewCommentForm(),
        "comments": comments,
    })


def index(request):
    if request.method == "POST":
        form = SearchingForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search"]
        searched = searchedList(query, AuctionListing.objects.all())
        return render(request, "auctions/index.html", {
        "form": SearchingForm(),
        "listings": searched
        })
    return render(request, "auctions/index.html", {
        "form": SearchingForm(),
        "listings": AuctionListing.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
