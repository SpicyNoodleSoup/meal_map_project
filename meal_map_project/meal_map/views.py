from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Restaurant


# This view is used to take all the restaurant objects in the database and
# show it in a list formate
class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/restaurant_list.html'  # Still need to adjust path
    context_object_name = 'restaurants'

# This view will get each the description of each restaurant object
    # DetailView will show all the information about the object
class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/restaurant_detail.html'  # Adjust path Later
    context_object_name = 'restaurant'
    
    
    
# Just the base html template, so i can see how it looks when im working on it - Luke
def base(request):
    
    response = render(request, 'meal_map/base.html')
    return response


def login(request):
    response = render(request, 'meal_map/login.html')
    return response

def homepage(request):
    response = render(request, 'meal_map/homepage.html')
    return response