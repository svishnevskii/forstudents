from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _



class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    bid = models.IntegerField()
    image = models.CharField(max_length=200, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    disable = models.BooleanField()

    #relation keys
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="winners")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")

    def __str__(self):
        return f"{self.title} {self.bid} seller:{self.user}"


class CategoryListing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="relation")

    class Meta:
        verbose_name = _("Relationship of categories")
        verbose_name_plural = _("Relationship of categories")


class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="viewed")

    def __str__(self):
        return f"{self.id}  listing:{self.listing}"
