from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Reviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="reviewer")
    profile_picture = models.ImageField(upload_to="reviewer_pics")

    class Meta:
        verbose_name_plural = "Reviewers"

    def __str__(self):
        return self.user.username

class RestaurantOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="restaurant_owner")
    profile_picture = models.ImageField(upload_to="owner_pics")

    def __str__(self):
        return self.user.username

class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    phone_number = models.CharField(max_length=32)
    opening_hours = models.CharField(max_length=128)
    website = models.URLField(max_length=128)
    rating = models.SmallIntegerField()
    food_type = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    photo = models.ImageField(upload_to="restaurant_photos")
    owner = models.OneToOneField(RestaurantOwner, on_delete=models.CASCADE, related_name='restaurant')

    def __str__(self):
        return self.name

class Review(models.Model):
    review_text = models.TextField()
    rating = models.SmallIntegerField()
    date = models.DateTimeField()
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return _("Review by {} on {}").format(self.reviewer, self.date)

## URL + images
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.user.username