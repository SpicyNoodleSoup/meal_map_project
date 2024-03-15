import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'meal_map_project.settings')

import django
django.setup()
from meal_map.models import Restaurant, Review, RestaurantOwner

def populate():
    # Creating a list of dictionaries for restaurant owners, restaurants and reviews.
    restaurant_owners = [
        {'email': 'owner1@example.com', 'restaurant_name': 'The Pizza Place', 'password': 'password1'},
        {'email': 'owner2@example.com', 'restaurant_name': 'The Burger House', 'password': 'password2'},
    ]
    
    restaurants_reviews = {
        'The Pizza Place': {
            'reviews': [
                {'text': 'Great pizza and excellent service!', 'rating': 5},
                {'text': 'Loved the ambiance, but the crust was too thick for my taste.', 'rating': 3},
                # Add more reviews for this restaurant.
            ],
            # Add other details for the restaurant as needed.
        },
        'The Burger House': {
            'reviews': [
                {'text': 'Best burgers in town!', 'rating': 5},
                {'text': 'Good prices but average taste.', 'rating': 3},
                # Add more reviews for this restaurant.
            ],
            # Add other details for the restaurant as needed.
        },
        # Add more restaurants and their reviews as needed.
    }
    
    # Add RestaurantOwners, Restaurants and Reviews to the database.
    for owner_data in restaurant_owners:
        owner = add_restaurant_owner(owner_data['email'], owner_data['restaurant_name'], owner_data['password'])
        
        if owner_data['restaurant_name'] in restaurants_reviews:
            restaurant_data = restaurants_reviews[owner_data['restaurant_name']]
            restaurant = add_restaurant(owner, owner_data['restaurant_name'])
            
            for review_data in restaurant_data['reviews']:
                add_review(restaurant, review_data['text'], review_data['rating'])

    # Print out the restaurants and reviews added.
    for r in Restaurant.objects.all():
        for review in Review.objects.filter(restaurant=r):
            print(f'- {r.name}: {review}')

def add_restaurant_owner(email, restaurant_name, password):
    owner, created = RestaurantOwner.objects.get_or_create(email=email, restaurant_name=restaurant_name)
    if created:
        owner.set_password(password)
        owner.save()
    return owner

def add_restaurant(owner, name):
    restaurant, created = Restaurant.objects.get_or_create(owner=owner, name=name)
    if created:
        # Set other details for the restaurant if needed.
        restaurant.save()
    return restaurant

def add_review(restaurant, text, rating):
    review, created = Review.objects.get_or_create(restaurant=restaurant, text=text, rating=rating)
    if created:
        review.save()
    return review

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
