from django.contrib import admin
from meal_map.models import UserProfile, Restaurant, Review, Reviewer


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Reviewer)
admin.site.register(Restaurant)
admin.site.register(Review)

