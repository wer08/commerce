from .models import User, AuctionListing, Watchlist, Comment, Bid

def checkWatchlist(request,listing):
    if request.user.is_authenticated:
        if Watchlist.objects.filter(listing = listing, user = request.user).exists():
            flag = True
        else:
            flag=False
    else:
        flag=False
    return flag

def getComments(listing):
    comments = Comment.objects.filter(listing = listing)
    return comments

def getWinner(listing):
    winning_bid = Bid.objects.filter(listing_id = listing).last()
    winner = winning_bid.bidder
    return winner