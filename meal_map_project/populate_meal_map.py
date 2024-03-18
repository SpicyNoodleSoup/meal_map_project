import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_map_project.settings')
from django.utils import timezone
import django
django.setup()
from django.contrib.auth.models import User
from meal_map.models import Restaurant, Review, RestaurantOwner, Reviewer
from django.core.files.base import ContentFile

def populate():
    # Users (Restaurant Owners and Reviewers)
    user_data = [
        {"username": "owner1", "email": "owner1@example.com", "password": "password1"},
        {"username": "owner2", "email": "owner2@example.com", "password": "password2"},
        {"username": "owner3", "email": "owner3@example.com", "password": "password3"},
        {"username": "owner4", "email": "owner4@example.com", "password": "password4"},
        {"username": "owner5", "email": "owner5@example.com", "password": "password5"},
        {"username": "owner6", "email": "owner6@example.com", "password": "password6"},
        {"username": "owner7", "email": "owner7@example.com", "password": "password7"},
        {"username": "owner8", "email": "owner8@example.com", "password": "password8"},
        {"username": "owner9", "email": "owner9@example.com", "password": "password9"},
        {"username": "owner10", "email": "owner10@example.com", "password": "password10"},
        {"username": "reviewer1", "email": "reviewer1@example.com", "password": "passwordreviewer1"},
        {"username": "reviewer2", "email": "reviewer2@example.com", "password": "passwordreviewer2"},
        {"username": "reviewer3", "email": "reviewer3@example.com", "password": "passwordreviewer3"},
        {"username": "reviewer4", "email": "reviewer4@example.com", "password": "passwordreviewer4"},
        {"username": "reviewer5", "email": "reviewer5@example.com", "password": "passwordreviewer5"},
    ]

    users = {ud["username"]: add_user(**ud) for ud in user_data}

    # Restaurants
    restaurant_data = [
        {"name": "The Pizza Place", "owner_username": "owner1", "description": "Best pizza in town.", "rating": 4, "food_type": "Italian", "location": "123 Main St", "image_filename": "pizza_place.jpg"},
        {"name": "Burger Joint", "owner_username": "owner2", "description": "Juicy burgers and crispy fries.", "rating": 4, "food_type": "American", "location": "456 Elm St","image_filename": "burger_place.jpg"},
        {"name": "Sushi Spot", "owner_username": "owner3", "description": "Fresh sushi and Japanese cuisine.", "rating": 5, "food_type": "Japanese", "location": "789 Oak Ave", "image_filename": "sushi_place.jpg"},
        {"name": "Taco City", "owner_username": "owner4", "description": "Authentic Mexican tacos and burritos.", "rating": 4, "food_type": "Mexican", "location": "321 Pine Rd", "image_filename": "taco_place.jpg"},
        {"name": "Pasta Palace", "owner_username": "owner5", "description": "Homemade pasta dishes and Italian specialties.", "rating": 4, "food_type": "Italian", "location": "654 Cedar Blvd", "image_filename": "pasta_place.jpg"},
        {"name": "Steak House", "owner_username": "owner6", "description": "Juicy steaks and classic American fare.", "rating": 5, "food_type": "Steakhouse", "location": "987 Maple Ln", "image_filename": "steak_meal.jpg"},
        {"name": "Seafood Shack", "owner_username": "owner7", "description": "Fresh seafood and coastal cuisine.", "rating": 4, "food_type": "Seafood", "location": "246 Ocean Dr", "image_filename": "seafood_meal.jpg"},
        {"name": "Thai Terrace", "owner_username": "owner8", "description": "Authentic Thai dishes and flavorful curries.", "rating": 5, "food_type": "Thai", "location": "135 Sunset Ave", "image_filename": "tai_place.jpg"},
        {"name": "Greek Grill", "owner_username": "owner9", "description": "Traditional Greek recipes and Mediterranean flavors.", "rating": 4, "food_type": "Greek", "location": "864 Olive St", "image_filename": "greek_place.jpg"},
        {"name": "Vegan Vibes", "owner_username": "owner10", "description": "Plant-based meals and healthy options.", "rating": 5, "food_type": "Vegan", "location": "579 Vine Rd", "image_filename": "vegan_place.jpg"},
    ]

    restaurants = {rd["name"]: add_restaurant(**rd, users=users) for rd in restaurant_data}

    # Reviews
    review_data = [
        {"text": "Amazing pizza! The crust was perfectly crispy.", "rating": 5, "restaurant_name": "The Pizza Place", "reviewer_username": "reviewer1"},
        {"text": "Great burgers and friendly service.", "rating": 4, "restaurant_name": "Burger Joint", "reviewer_username": "reviewer2"},
        {"text": "The sushi was so fresh and delicious.", "rating": 5, "restaurant_name": "Sushi Spot", "reviewer_username": "reviewer3"},
        {"text": "Authentic Mexican flavors. The tacos were outstanding.", "rating": 4, "restaurant_name": "Taco City", "reviewer_username": "reviewer4"},
        {"text": "The pasta dishes were homemade and tasty.", "rating": 4, "restaurant_name": "Pasta Palace", "reviewer_username": "reviewer5"},
        {"text": "The steak was cooked to perfection. Highly recommended.", "rating": 5, "restaurant_name": "Steak House", "reviewer_username": "reviewer1"},
        {"text": "Fresh seafood and great coastal ambiance.", "rating": 4, "restaurant_name": "Seafood Shack", "reviewer_username": "reviewer2"},
        {"text": "The Thai curries were flavorful and spicy. Loved it!", "rating": 5, "restaurant_name": "Thai Terrace", "reviewer_username": "reviewer3"},
        {"text": "Authentic Greek flavors. The gyros were delicious.", "rating": 4, "restaurant_name": "Greek Grill", "reviewer_username": "reviewer4"},
        {"text": "Fantastic vegan options. The plant-based burgers were amazing.", "rating": 5, "restaurant_name": "Vegan Vibes", "reviewer_username": "reviewer5"},
        {"text": "Decent pizza, but I've had better.", "rating": 3, "restaurant_name": "The Pizza Place", "reviewer_username": "reviewer2"},
        {"text": "The burgers were a bit dry, but the fries were good.", "rating": 3, "restaurant_name": "Burger Joint", "reviewer_username": "reviewer3"},
        {"text": "Average sushi. Nothing extraordinary.", "rating": 3, "restaurant_name": "Sushi Spot", "reviewer_username": "reviewer4"},
        {"text": "The tacos were okay, but not the best I've had.", "rating": 3, "restaurant_name": "Taco City", "reviewer_username": "reviewer5"},
        {"text": "The pasta was overcooked and lacked flavor.", "rating": 2, "restaurant_name": "Pasta Palace", "reviewer_username": "reviewer1"},
        {"text": "The steak was tough and not worth the price.", "rating": 2, "restaurant_name": "Steak House", "reviewer_username": "reviewer2"},
        {"text": "Disappointing seafood. Not fresh and overpriced.", "rating": 2, "restaurant_name": "Seafood Shack", "reviewer_username": "reviewer3"},
        {"text": "The Thai food was too sweet and not authentic.", "rating": 2, "restaurant_name": "Thai Terrace", "reviewer_username": "reviewer4"},
        {"text": "The Greek dishes were bland and uninspired.", "rating": 2, "restaurant_name": "Greek Grill", "reviewer_username": "reviewer5"},
        {"text": "Limited vegan options. The dishes lacked creativity.", "rating": 2, "restaurant_name": "Vegan Vibes", "reviewer_username": "reviewer1"},
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

def add_restaurant(name, owner_username, description, rating, food_type, location, users, image_filename):
    owner_user = users[owner_username]
    owner, _ = RestaurantOwner.objects.get_or_create(user=owner_user)
    restaurant, _ = Restaurant.objects.get_or_create(
        name=name,
        owner=owner,
        defaults={
            'description': description,
            'rating': rating,
            'food_type': food_type,
            'location': location,
        }
    )

    if image_filename:
        with open(f"media/restaurant_photos/{image_filename}", "rb") as f:
            content = f.read()
        restaurant.photo.save(image_filename, ContentFile(content), save=False)
        restaurant.save()

    return restaurant

def add_review(text, rating, restaurant_name, reviewer_username, users, restaurants):
    reviewer_user = users[reviewer_username]
    reviewer, _ = Reviewer.objects.get_or_create(user=reviewer_user)
    restaurant = restaurants[restaurant_name]
    review_date = timezone.now()
    review, _ = Review.objects.get_or_create(
        review_text=text,
        rating=rating,
        reviewer=reviewer,
        restaurant=restaurant,
        date=review_date
    )

if __name__ == '__main__':
    print('Starting meal map population script...')
    populate()