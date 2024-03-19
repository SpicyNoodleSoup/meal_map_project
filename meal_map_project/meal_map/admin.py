from django.contrib import admin
from meal_map.models import Restaurant, Review, Reviewer, RestaurantOwner


# Register your models here.
admin.site.register(Reviewer)
admin.site.register(RestaurantOwner)
admin.site.register(Restaurant)
admin.site.register(Review)
