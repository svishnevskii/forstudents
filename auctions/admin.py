from django.contrib import admin
from .models import User, Listing, Watchlist, Category, CategoryListing, Comment

# Register your models here.

class CategoryListingAdmin(admin.ModelAdmin):
    list_display = ("category", "listing")

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Category)
admin.site.register(CategoryListing, CategoryListingAdmin)
admin.site.register(Comment)
