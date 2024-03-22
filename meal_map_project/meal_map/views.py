from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Restaurant, RestaurantOwner, Review, Reviewer
from .forms import AddRestaurantForm, AddReviewForm, ReviewerForm, RestaurantOwnerForm
from django.db.models import Avg



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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if not hasattr(user, "reviewer"):
                    Reviewer.objects.create(user=user)
                return redirect(reverse('meal_map:homepage'))
            else:
                messages.error(request, "Your Rango Meal Map is disabled.")
                return redirect('meal_map:login')  # Use your login view's URL name here
        else:
            messages.error(request, "Invalid login details supplied.")
            return redirect('meal_map:login')  # Use your login view's URL name here
    else:
        return render(request, 'meal_map/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('meal_map:homepage')

def homepage(request):
    top_restaurants = Restaurant.objects.annotate(
        average_rating=Avg('reviews__rating')
    ).order_by('-average_rating')[:15]  # Get top 15 restaurants by rating

    new_restaurants = Restaurant.objects.annotate(average_rating=Avg('reviews__rating')).order_by('-id')[:15]

    categories = ['Desserts', 'Bryans Steak', 'Vietnamese', 'Thai', 'Spanish', 'Japanese', 'Seafood',
                  'Sandwiches', 'Salad', 'Pizza', 'Mexican', 'American', 'Italian', 'Indian', 'Vegan', 
                  'Greek','German', 'French', 'Fast Food', 'Exotic', 'Ethiopian', 'European', 'Eastern European',
                  'Diner', 'Cuban', 'Coffee and Tea', 'Chinese', 'Caribbean', 'Burgers', 'Breakfast',
                  'Bar Food', 'Bakery', 'Barbeque']
    
    category_restaurants = {}
    for category in categories:
        restaurants = Restaurant.objects.filter(food_type__icontains=category).annotate(
            average_rating=Avg('reviews__rating')).order_by('-average_rating')[:15]
        category_restaurants[category] = restaurants
    
    context = {
        'top_restaurants': top_restaurants,
        'new_restaurants': new_restaurants,
        'category_restaurants': category_restaurants,
    }
    
    return render(request, 'meal_map/homepage.html', context)

@login_required
def my_account(request):
    try:
        reviewer_instance = request.user.reviewer
        recent_reviews = Review.objects.filter(reviewer=reviewer_instance).order_by('-date')[:2]
        all_reviews = Review.objects.filter(reviewer=reviewer_instance).order_by('-date')
        context = {
            'recent_reviews': recent_reviews,
            'all_reviews': all_reviews,
        }
    except Reviewer.DoesNotExist:
        context = {}

    return render(request, 'meal_map/account.html', context)


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
    

@login_required
def my_reviews(request):
    try:
        reviewer_instance = request.user.reviewer
        all_reviews = Review.objects.filter(reviewer=reviewer_instance).order_by('-date')
        context = {
            'all_reviews': all_reviews,
        }
    except Reviewer.DoesNotExist:
        context = {}

    return render(request, 'meal_map/my_reviews.html', context)
        
def register(request):
    if request.method == 'POST':
        if 'register_reviewer' in request.POST:
            reviewer_form = ReviewerForm(request.POST, request.FILES)
            username = request.POST.get('username')
            if User.objects.filter(username=username).exists():
                reviewer_form = ReviewerForm()
                restaurant_form = RestaurantOwnerForm()
                return render(request, 'meal_map/register.html', context={'error_message': 'Username already exists', 'reviewer_form': reviewer_form, 'restaurant_form': restaurant_form,})
            if reviewer_form.is_valid():
                user = reviewer_form.save()
                login(request, user)
                return redirect('meal_map:homepage')
            else:
                print(reviewer_form.errors)
        elif 'register_restaurant_owner' in request.POST:
            restaurant_form = RestaurantOwnerForm(request.POST, request.FILES)
            username = request.POST.get('username')
            if User.objects.filter(username=username).exists():
                reviewer_form = ReviewerForm()
                restaurant_form = RestaurantOwnerForm()
                return render(request, 'meal_map/register.html', context={'error_message': 'Username already exists', 'reviewer_form': reviewer_form, 'restaurant_form': restaurant_form,})
            if restaurant_form.is_valid():
                user = restaurant_form.save()
                login(request, user)
                return redirect('meal_map:homepage')
            else:
                print(restaurant_form.errors)
    else:
        reviewer_form = ReviewerForm()
        restaurant_form = RestaurantOwnerForm()

    return render(request, 'meal_map/register.html',
                  context = {'reviewer_form': reviewer_form,
                             'restaurant_form': restaurant_form,})

def restaurant(request, restaurant_name_slug):
    context_dict = {}
        
    try:
        restaurant = Restaurant.objects.get(slug=restaurant_name_slug)
        reviews = Review.objects.filter(restaurant=restaurant)
        average_rating = restaurant.calculate_rating()
        
        if request.method == 'POST':
            review_form = AddReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.restaurant = restaurant
                if hasattr(request.user, 'reviewer'):
                    review.reviewer = request.user.reviewer
                    review.date = timezone.now()
                    review.save()
                return redirect('meal_map:show_restaurant', restaurant_name_slug=restaurant.slug)
            
        else:
            review_form = AddReviewForm()
        
        context_dict['restaurant'] = restaurant
        context_dict['reviews'] = reviews
        context_dict['review_form'] = review_form
        context_dict['average_rating'] = average_rating
    except Restaurant.DoesNotExist:
        context_dict['restaurant'] = None
        context_dict['reviews'] = None
        context_dict['review_form'] = AddReviewForm()
        
    return render(request, 'meal_map/restaurant.html', context=context_dict)
    
@login_required
def update_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')
        
        user = request.user
        user.username = username
        user.email = email
        user.save()
        
        if hasattr(user, 'reviewer'):
            reviewer = user.reviewer
            if profile_picture:
                reviewer.profile_picture = profile_picture
                reviewer.save()
        elif hasattr(user, 'restaurant_owner'):
            restaurant_owner = user.restaurant_owner
            if profile_picture:
                restaurant_owner.profile_picture = profile_picture
                restaurant_owner.save()
        
        return redirect('meal_map:my_account')
    else:
        return redirect('meal_map:my_account')


