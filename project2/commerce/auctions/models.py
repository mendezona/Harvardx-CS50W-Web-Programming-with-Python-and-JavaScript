from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

#Abstract user carries fields for username, email, and password
class User(AbstractUser):
    pass

#create table for listings showing title, description, starting price, category, image, associated user
#models.ForeignKey denotes one to many relationship, eg one listing can have many bids
class Listing(models.Model):
    listingTitle = models.CharField(max_length=100)
    listingDesc = models.CharField(max_length=2000)
    listingPrice = models.DecimalField(max_digits=20, decimal_places=2)
    listingCategory = models.CharField(max_length=100)
    listingImage = models.CharField(max_length=300, blank=True)
    listingUser = models.ForeignKey(User, on_delete=models.CASCADE)
    listingActive = models.BooleanField(default=True)
    listingCreated = models.DateTimeField(default=timezone.now(), blank=True)

    def __str__(self):
        return f"title: {self.listingTitle}, desc: {self.listingDesc}, price: {self.listingPrice}, price: {self.listingCategory}, price: {self.listingImage}, price: {self.listingUser} "

class Bids(models.Model):
    biddingUser = models.ForeignKey(User, on_delete=models.CASCADE)
    bidPrice = models.DecimalField(max_digits=20, decimal_places=2)
    bidListing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidSubmitted = models.DateTimeField(default=timezone.now(), blank=True)

class Comments(models.Model):
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentListing = models.ForeignKey(Listing, on_delete=models.CASCADE) 
    commentText = models.CharField(max_length=500)
    commentSubmitted = models.DateTimeField(default=timezone.now(), blank=True)

class Watchlist(models.Model):
    watchlistListingID = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watchlistUserID = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlistActive = models.BooleanField(default=False)

class Winners(models.Model):
    winnerUser = models.ForeignKey(User, on_delete=models.CASCADE)
    winningPrice = models.DecimalField(max_digits=20, decimal_places=2)
    winningBidId = models.ForeignKey(Listing, on_delete=models.CASCADE)
