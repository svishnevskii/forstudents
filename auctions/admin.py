from django.contrib import admin
from .models import User, Listing, Watchlist, Category, Winner, CategoryListing

# Register your models here.

class CategoryListingAdmin(admin.ModelAdmin):
    list_display = ("category", "listing")

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Category)
admin.site.register(Winner)
admin.site.register(CategoryListing, CategoryListingAdmin)
