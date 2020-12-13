from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

#import models and forms
from .models import User, Listing, Bids, Comments, Watchlist, Winners
from django import forms

#add timezone stamping support for various models
from django.utils import timezone

#add support to display pricing on index page
from django.template.defaulttags import register

#support to display dictionaries and tuples in HTML pages
@register.filter
def keyvalue(dict, key):    
    return dict[key]

@register.filter
def tuplevalue(tuple, index):    
    return tuple[index]


def index(request):
    listings = Listing.objects.all()

    #create a dictionary of prices to refer to in order to display most up to date prices
    priceDict = {}
    for listing in listings:
        if listing.listingActive == True:
            item = Listing.objects.get(id=listing.id)

             #check if any bids have been placed
            highestBid = Bids.objects.filter(bidListing=item).order_by('-bidPrice').first()

            #if no bids have been placed display listing price, else display highest bid
            if highestBid == None:
                price = item.listingPrice

            else:
                price = highestBid.bidPrice

            priceDict[listing.id] = round(price, 2)

    return render(request, "auctions/index.html", {
        "listings": listings,
        "prices": priceDict
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

#form for new listing
class newListing(forms.Form):
    categories = (
        ("1", "Electronics"),
        ("2", "Entertainment"),
        ("3", "Fashion"),
        ("4", "Food"),
        ("5", "Home"),
        ("6", "Office"),
        ("7", "Outdoors"),
        ("8", "Toys"),
    )

    listingTitle = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control my-2'}), label="Title")
    listingDesc = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'class': 'form-control my-2'}), label="Description")
    listingPrice = forms.DecimalField(max_digits=20, widget=forms.TextInput(attrs={'class': 'form-control my-2'}), decimal_places=2, label="Starting price")
    listingCategory = forms.ChoiceField(choices=categories, widget=forms.Select(attrs={'class': 'form-control my-2'}), label="Category")
    listingImage = forms.CharField(max_length=300, required=False, widget=forms.TextInput(attrs={'class': 'form-control my-2'}), label="Image URL (optional)")


#if user goes to new listing page
def newlisting(request):
    #get form to submit item
    if request.method == "GET":
        return render(request, "auctions/newlisting.html", {
            "newListingForm": newListing(),
            "test": Listing.objects.all()
        })

    #if form is filled, add listing to database and redirect to active listings
    else:

        #add listing to databse
        form = newListing(request.POST)
        if form.is_valid():
            listingTitle = form.cleaned_data["listingTitle"].capitalize()
            listingDesc = form.cleaned_data["listingDesc"]
            listingPrice = form.cleaned_data["listingPrice"]
            listingCategory = form.cleaned_data["listingCategory"]
            listingImage = form.cleaned_data["listingImage"]
            listingUser = User.objects.get(username=request.user.username)
            
            newEntry = Listing(listingTitle=listingTitle, listingDesc=listingDesc, listingPrice=listingPrice, listingCategory=listingCategory, listingImage=listingImage, listingUser=listingUser)
            newEntry.save()

        return HttpResponseRedirect(reverse("index"))


#form for new bid
class newBid(forms.Form):
    bidPrice = forms.DecimalField(max_digits=20, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Bid'}), label='')


#form for comments
class commentForm(forms.Form):
    commentText = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Enter comment here'}), label='')


#process comments after submitted on listing page and redirect back to page
def comment(request):
    form = commentForm(request.GET)
    if form.is_valid():
        commentText = form.cleaned_data["commentText"]
        commentUser = User.objects.get(id=request.GET["userId"])
        commentListing = Listing.objects.get(id=request.GET["itemId"])

        newComment = Comments(commentText=commentText, commentUser=commentUser, commentListing=commentListing)
        newComment.save()

    return HttpResponseRedirect(reverse("listing", kwargs = {"listing_id":request.GET["itemId"]}))


#get listing_id and lookup page for it
def listing(request, listing_id):

    item = Listing.objects.get(id=listing_id)
    status = ''

    #check if any bids have been placed
    highestBid = Bids.objects.filter(bidListing=item).order_by('-bidPrice').first()

    #if no bids have been placed display listing price, else display highest bid
    if highestBid == None:
        price = item.listingPrice

    else:
        price = highestBid.bidPrice

    #if auction is over get winner
    winner = ''
    if item.listingActive == False:
        winnerUsername = Winners.objects.get(winningBidId=listing_id)
        winner = winnerUsername.winnerUser_id

    #get comments
    comments = Comments.objects.filter(commentListing=listing_id)

    if request.method == "GET":
        pass

    #after user submits a bid
    else:
        #get data from form and ensure validity
        form = newBid(request.POST)
        if form.is_valid():
            bidPrice = form.cleaned_data["bidPrice"]
            biddingUser = User.objects.get(id=int(request.POST["userId"]))
            bidListing = Listing.objects.get(id=int(request.POST["itemId"]))

            #check if any bids have been placed
            highestBid = Bids.objects.filter(bidListing=bidListing).order_by('-bidPrice').first()

            #if no bids have been placed, ensure first bid is equal or greater than the listing price and save
            if highestBid == None:
                originalListing = Listing.objects.get(id=int(request.POST["itemId"]))
                if bidPrice >= originalListing.listingPrice:
                    firstBid = Bids(biddingUser=biddingUser, bidPrice=bidPrice, bidListing=bidListing)
                    firstBid.save()
                    status = "Bid successfully placed."

                #present error if it does not meet
                else:
                    status = "Bid does not meet the listing price for this auction."

            #if a bid has been placed previously, ensure new bid is higher than previous bid
            else:
                if bidPrice > highestBid.bidPrice:
                    newHighBid = Bids(biddingUser=biddingUser, bidPrice=bidPrice, bidListing=bidListing)
                    newHighBid.save()
                    status = "Bid successfully placed."

                #present error if bid does not exceed the current bid
                else:
                    status = "Bid does not exceed current bid placed for this auction."

    return render(request, "auctions/listing.html", {
        "item": item,
        "bidForm": newBid(),
        "price": price,
        "bidsCount": Bids.objects.filter(bidListing=item).count(),
        "winner": winner,
        "comments": comments,
        "commentForm": commentForm,
        "status": status
    })


#Generate a user's watchlist
def watchlist(request):
    #get all watchlisted items for current user
    current_user = request.user
    watchListObjects = Watchlist.objects.filter(watchlistUserID=current_user.id, watchlistActive=True)

    #create a dictionary of items to display
    items = {}
    for instance in watchListObjects:
        item = Listing.objects.get(id=instance.id)
        items[instance.id] = instance.watchlistListingID

    return render(request, "auctions/watchlist.html", {
        "listings": items.values(),
    })


#watchlist toggle
def watchlistToggle(request):
    if request.method == "GET":

        #if watchlist entry already exists, flip the watchlist boolean for item belonging to user
        try:
            existingSave = Watchlist.objects.get(watchlistListingID=Listing.objects.get(id=int(request.GET["itemId"])), watchlistUserID=User.objects.get(username=request.user.username))
            newBoolean = not existingSave.watchlistActive
            Watchlist.objects.filter(watchlistListingID=Listing.objects.get(id=int(request.GET["itemId"])), watchlistUserID=User.objects.get(username=request.user.username)).update(watchlistActive=newBoolean)
            
        #create and save item to watchlist if user has clicked watchlist for first time
        except Watchlist.DoesNotExist:
            newSave = Watchlist(watchlistListingID=Listing.objects.get(id=int(request.GET["itemId"])), watchlistUserID=User.objects.get(username=request.user.username), watchlistActive=True)
            newSave.save()

        #redirect to watchlist once processed
        return HttpResponseRedirect(reverse("watchlist"))


#user closes auction, saves record of winner and removes active state to remove from active listings
def closeauction(request):
    if request.method == "GET":
        itemId = request.GET["itemId"]
        highestBidder = Bids.objects.filter(bidListing=int(request.GET["itemId"])).order_by('-bidPrice').first()

        winner = Winners(winnerUser=User.objects.get(username=highestBidder.biddingUser), winningPrice=highestBidder.bidPrice, winningBidId=Listing.objects.get(id=itemId))
        winner.save()

        Listing.objects.filter(id=int(request.GET["itemId"])).update(listingActive=False)
        return HttpResponseRedirect(reverse("listing", kwargs = {"listing_id":itemId}))


#category form
class selectCategory(forms.Form):
    categories = newListing.categories
    filterCategory = forms.ChoiceField(choices=categories, widget=forms.Select(attrs={'class': 'form-control my-2'}), label="Category")

#generate page for user to filter page by categories
def categories(request):
    if request.method == "GET":
        return render(request, "auctions/categories.html", {
        "categories": selectCategory
    })

    else:
        form = selectCategory(request.POST)
        if form.is_valid():
            listingCategory = form.cleaned_data["filterCategory"]
            listings = Listing.objects.filter(listingCategory=listingCategory, listingActive=True)

            #create a dictionary of prices to refer to in order to display most up to date prices
            priceDict = {}
            for listing in listings:
                if listing.listingActive == True:
                    item = Listing.objects.get(id=listing.id)

                    #check if any bids have been placed
                    highestBid = Bids.objects.filter(bidListing=item).order_by('-bidPrice').first()

                    #if no bids have been placed display listing price, else display highest bid
                    if highestBid == None:
                        price = item.listingPrice

                    else:
                        price = highestBid.bidPrice

                    priceDict[listing.id] = round(price, 2)

        return render(request, "auctions/categories.html", {
            "categories": selectCategory,
            "listings": listings,
            "prices": priceDict
        })