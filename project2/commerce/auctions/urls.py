from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("closeauction", views.closeauction, name="closeauction"),
    path("comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlistToggle", views.watchlistToggle, name="watchlistToggle"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
