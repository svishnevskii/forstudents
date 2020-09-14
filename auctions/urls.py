from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings/<int:category_id>/category", views.category, name="category"),
    #
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/add", views.add_watchlist, name="add_watchlist"),
    path("watchlist/<int:listing_id>/delete", views.delete_watchlist, name="delete_watchlist"),

    #Place bid
    path("listing/bid/open" , views.bid_open, name="placebid")
]
