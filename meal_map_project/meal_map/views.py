from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Restaurant, RestaurantOwner
from .forms import UserForm, UserProfileForm, AddRestaurantForm



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


def user_login(request):
    # response = render(request, 'meal_map/login.html')
    # return response
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('meal_map:homepage'))
            else:
                return HttpResponse("Your Rango Meal Map is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'meal_map/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('meal_map:homepage')

def homepage(request):
    top_restaurants = Restaurant.objects.order_by('-rating')[:15]  # Get top 15 restaurants by rating
    new_restaurants = Restaurant.objects.order_by('-id')[:15]

    categories = ['Desserts', 'Bryans Steak', 'Vietnamese', 'Thai', 'Spanish', 'Soul Food', 'Seafood',
                  'Sandwiches', 'Salad', 'Pizza', 'Mexican', 'Italian', 'Indian', 'Healthy Food', 'Greek',
                  'German', 'French', 'Fast Food', 'Exotic', 'Ethiopian', 'European', 'Eastern European',
                  'Diner', 'Cuban', 'Coffee and Tea', 'Chinese', 'Caribbean', 'Burgers', 'Breakfast',
                  'Bar Food', 'Bakery', 'Barbeque']
    
    category_restaurants = {}
    for category in categories:
        restaurants = Restaurant.objects.filter(food_type__icontains=category).order_by('-rating')[:15]
        category_restaurants[category] = restaurants
    
    context = {
        'top_restaurants': top_restaurants,
        'new_restaurants': new_restaurants,
        'category_restaurants': category_restaurants,
    }
    
    return render(request, 'meal_map/homepage.html', context)

def my_account(request):
    response = render(request, 'meal_map/account.html')
    return response

@login_required
def add_restaurant(request):
    form = AddRestaurantForm()
    if request.method == 'POST':
        form = AddRestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            try:
                restaurant_owner_profile = request.user.restaurant_owner
                restaurant.owner = restaurant_owner_profile
                restaurant.save()
                return redirect('meal_map:homepage')
            except RestaurantOwner.DoesNotExist:
                form.add_error(None, "Current user does not have a restaurant owner profile.")

            return redirect('meal_map:homepage')
        else:
            print(form.errors)
            
    return render(request,'meal_map/add_restaurant.html', {'form':form})
    

def my_reviews(request):
    response = render(request, 'meal_map/my_reviews.html')
    return response

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'meal_map/register.html', {'error_message': 'Username already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        login(request, user)
        
        return redirect('meal_map:homepage')
    else:
        return render(request, 'meal_map/register.html')
    
def restaurant_register(request):
    if request.method == 'POST':
        restaurant_name = request.POST['restaurantName']
        owner_name = request.POST['ownerName']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=owner_name).exists():
            return render(request, 'meal_map/register.html', {'error_message': 'Username already exists'})
    
        user = User.objects.create_user(username=owner_name, email=email, password=password)

        login(request, user)
        
        return redirect('meal_map:homepage')
    else:
        return render(request, 'meal_map/restaurant_register.html')

def restaurant(request):
    response = render(request, 'meal_map/restaurant.html')
    return response