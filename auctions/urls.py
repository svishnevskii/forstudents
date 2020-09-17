from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    path("my/listings/", views.mylistings, name="mylistings"),
    path("my/bids/", views.mybids, name="mybids"),
    path("my/listings/create", views.listing_create, name="listing_create"),

    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings/<int:category_id>/category", views.category, name="category"),
    path("comment/<int:listing_id>", views.comment, name="comment"),


    #
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/add", views.add_watchlist, name="add_watchlist"),
    path("watchlist/<int:listing_id>/delete", views.delete_watchlist, name="delete_watchlist"),

    #Place bid
    path("listing/bid/open" , views.bid_open, name="placebid"),
    path("listing/bid/close" , views.bid_close, name="closebid")
]
