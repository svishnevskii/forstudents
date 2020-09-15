from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, CategoryListing, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().filter(disable=False),
        "categories" : Category.objects.all()
    })

def mylistings(request):
    return render(request, "auctions/personal/listings.html", {
        "listings": request.user.listing.all(),
        "categories" : Category.objects.all()
    })

def mybids(request):
    return render(request, "auctions/personal/listings.html", {
        "listings": Listing.objects.filter(winner=request.user.id).all(),
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

    has_watchlist = False if not request.user.is_authenticated else Watchlist.objects.filter(listing=listing_id, user=request.user)

    #Check Alerts
    if request.session.get('alert'):
        alert = request.session.get('alert')
        request.session['alert'] = ""
    else:
        alert = ""



    return render(request, "auctions/listing.html", {
        "listing": listing,
        "categories": categories,
        "has_watchlist": has_watchlist,
        "has_alert": alert
    })

#Current category
def category(request, category_id):
    """
    CategoryListing is relation table between Category and Listing models.
    """
    category = Category.objects.filter(pk=category_id)

    if category.exists():
        categories = CategoryListing.objects.filter(category=category_id)
    else:
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/category.html", {
        "category": category.get(),
        "categories": categories,
    })


#Watchlist Actions
def add_watchlist(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    current = Listing.objects.get(id = listing_id)
    w = Watchlist(listing_id=current.id, user_id=request.user.id)
    w.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))



def delete_watchlist(request, listing_id):
    if request.user.is_authenticated:
        request.user.viewed.filter(listing_id=listing_id).delete()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def watchlist(request):
    # return HttpResponse(request.user.viewed.first().listing.title)
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.viewed.all(),
        "categories" : Category.objects.all()
    })

#Bid Actions [open, close]
def bid_close(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        #todo factory
        winner_id = int(request.POST.get('winner_id'))
        listing_id = int(request.POST.get('listing_id'))


        #Проверим существует ли передаваемы победитель
        winner = has_user = User.objects.filter(pk=winner_id)
        if not has_user:
            return HttpResponseRedirect(reverse("login"))
        else:
            list = Listing.objects.filter(pk=listing_id, winner=winner.get().id).get()
            list.disable = True # Close positin for bid
            list.save()

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def bid_open(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        request.session['alert'] = ""

        bid = int(request.POST.get('bid'))
        lising_id = int(request.POST.get('listing_id'))

        current = Listing.objects.get(pk=lising_id)

        if current.bid < bid:
            current.bid = bid
            current.winner = User.objects.get(pk=request.user.id)
            current.save()
        else:
            request.session['alert'] = f"The rate must be higher than the ${current.bid} price"

        return HttpResponseRedirect(reverse("listing", args=[current.id]))
    else:
        return HttpResponseRedirect(reverse("index"))
