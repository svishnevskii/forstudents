from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, CategoryListing, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "categories" : Category.objects.all()
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

#Single Card
def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        categories = listing.relation.all()
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")

    has_watchlist = Watchlist.objects.filter(
            listing_id=listing_id, user=request.user)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "categories": categories,
        "has_watchlist": has_watchlist
    })

#Current category
def category(request, category_id):
    """
    CategoryListing is relation table between Category and Listing models.
    """
    try:
        categories = CategoryListing.objects.filter(category=category_id)
    except CategoryListing.DoesNotExist:
        raise Http404("Category not found.")

    return render(request, "auctions/category.html", {
        "category": categories.first().category,
        "categories": categories,
    })

#Filtered list
def watchlist(request, listing_id = None):
    if request.user.is_authenticated:
        #Если товар не добавляется в watchlist
        if not listing_id:
            #Берём watchlist авторизованного пользователя
            watchlist = Watchlist.objects.filter(user_id=request.user.id)
            return render(request, "auctions/watchlist.html", {
                "watchlist": watchlist
            })
        else:
            #Существует ли такой Listing
            exists = Watchlist.objects.get(listing=listing_id)
            if not exists:
                listening = Listing.objects.get(id=listing_id)
                #Добавляем Listing в Watchlist пользователя
                w = Watchlist(listing=listening, user=request.user)
                w.save()
            else:
                return Http404("Not found.")
    else:
        return HttpResponseRedirect(reverse("login"))
