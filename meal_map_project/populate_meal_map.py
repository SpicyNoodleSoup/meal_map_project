import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_map_project.settings')
from django.utils import timezone

import django
django.setup()
from django.contrib.auth.models import User
from meal_map.models import Restaurant, Review, RestaurantOwner, Reviewer

def populate():
    # Users (Restaurant Owners and Reviewers)
    user_data = [
        {"username": "owner1", "email": "owner1@example.com", "password": "password1"},
        {"username": "reviewer1", "email": "reviewer1@example.com", "password": "passwordreviewer1"},
        # Add more user data as needed
    ]

    users = {ud["username"]: add_user(**ud) for ud in user_data}

    # Restaurants
    restaurant_data = [
        {"name": "The Pizza Place", "owner_username": "owner1", "description": "Best pizza in town."},
        # Add more restaurant data as needed
    ]

    restaurants = {rd["name"]: add_restaurant(**rd, users=users) for rd in restaurant_data}

    # Reviews
    review_data = [
        {"text": "Great pizza!", "rating": 5, "restaurant_name": "The Pizza Place", "reviewer_username": "reviewer1"},
        # Add more review data as needed
    ]

    for rd in review_data:
        add_review(**rd, users=users, restaurants=restaurants)

    # Print out what has been added
    for r in Restaurant.objects.all():
        for review in Review.objects.filter(restaurant=r):
            print(f'- {r.name}: {review}')

def add_user(username, email, password):
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)
        user.save()
    return user

def add_restaurant(name, owner_username, description, users):
    owner_user = users[owner_username]
    owner, _ = RestaurantOwner.objects.get_or_create(user=owner_user)
    # Ensure you provide a default value for the 'rating' field here
    default_rating = 0  # Or any other default rating appropriate for your application logic
    restaurant, _ = Restaurant.objects.get_or_create(name=name, owner=owner, description=description, rating=default_rating)
    return restaurant



def add_review(text, rating, restaurant_name, reviewer_username, users, restaurants):
    reviewer_user = users[reviewer_username]
    reviewer, _ = Reviewer.objects.get_or_create(user=reviewer_user)
    restaurant = restaurants[restaurant_name]
    # Provide a default value for the 'date' field here, for example, using timezone.now()
    review_date = timezone.now()  # This sets the review date to the current date and time
    review, _ = Review.objects.get_or_create(
        review_text=text,
        rating=rating,
        reviewer=reviewer,
        restaurant=restaurant,
        date=review_date  # Ensure to include this date in the function call
    )


if __name__ == '__main__':
    print('Starting meal map population script...')
    populate()
