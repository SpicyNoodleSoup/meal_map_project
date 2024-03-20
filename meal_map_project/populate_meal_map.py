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
        {"username": "johnsmith", "email": "johnsmith@example.com", "password": "password1"},
        {"username": "sarahjones", "email": "sarahjones@example.com", "password": "password2"},
        {"username": "mikebrown", "email": "mikebrown@example.com", "password": "password3"},
        {"username": "emilydavis", "email": "emilydavis@example.com", "password": "password4"},
        {"username": "davidmiller", "email": "davidmiller@example.com", "password": "password5"},
        {"username": "oliviawilson", "email": "oliviawilson@example.com", "password": "password6"},
        {"username": "jamesjohnson", "email": "jamesjohnson@example.com", "password": "password7"},
        {"username": "sophiebrown", "email": "sophiebrown@example.com", "password": "password8"},
        {"username": "williamsmith", "email": "williamsmith@example.com", "password": "password9"},
        {"username": "oliverjones", "email": "oliverjones@example.com", "password": "password10"},
        {"username": "issacnewton", "email": "issacnewton@example.com", "password": "passwordreviewer1"},
        {"username": "galileogalilei", "email": "galileogalilei@example.com", "password": "passwordreviewer2"},
        {"username": "alberteinstein", "email": "alberteinstein@example.com", "password": "passwordreviewer3"},
        {"username": "mariamcurie", "email": "mariamcurie@example.com", "password": "passwordreviewer4"},
        {"username": "charlesdarwin", "email": "charlesdarwin@example.com", "password": "passwordreviewer5"},
    ]

    users = {ud["username"]: add_user(**ud) for ud in user_data}

    # Restaurants
    restaurant_data = [
        {"name": "The Pizza Place", "owner_username": "johnsmith", "description": "Best pizza in town.", "rating": 4, "food_type": "Italian", "location": "123 Main St", "image_filename": "pizza_place.jpg", "phone_number": "123-456-7890", "opening_hours": "Mon-Fri: 11am-10pm, Sat-Sun: 12pm-11pm", "website": "https://www.thepizzaplace.com"},
        {"name": "Burger Joint", "owner_username": "sarahjones", "description": "Juicy burgers and crispy fries.", "rating": 4, "food_type": "American", "location": "456 Elm St", "image_filename": "burger_place.jpg", "phone_number": "987-654-3210", "opening_hours": "Mon-Thu: 10am-9pm, Fri-Sat: 10am-11pm, Sun: 11am-8pm", "website": "https://www.burgerjoint.com"},
        {"name": "Sushi Spot", "owner_username": "mikebrown", "description": "Fresh sushi and Japanese cuisine.", "rating": 5, "food_type": "Japanese", "location": "789 Oak Ave", "image_filename": "sushi_place.jpg", "phone_number": "555-123-4567", "opening_hours": "Tue-Sun: 11:30am-2:30pm, 5pm-10pm", "website": "https://www.sushispot.com"},
        {"name": "Taco City", "owner_username": "emilydavis", "description": "Authentic Mexican tacos and burritos.", "rating": 4, "food_type": "Mexican", "location": "321 Pine Rd", "image_filename": "taco_place.jpg", "phone_number": "111-222-3333", "opening_hours": "Mon-Sat: 11am-9pm", "website": "https://www.tacocity.com"},
        {"name": "Pasta Palace", "owner_username": "davidmiller", "description": "Homemade pasta dishes and Italian specialties.", "rating": 4, "food_type": "Italian", "location": "654 Cedar Blvd", "image_filename": "pasta_place.jpg", "phone_number": "444-555-6666", "opening_hours": "Wed-Sun: 5pm-11pm", "website": "https://www.pastapalace.com"},
        {"name": "Steak House", "owner_username": "oliviawilson", "description": "Juicy steaks and classic American fare.", "rating": 5, "food_type": "Steakhouse", "location": "987 Maple Ln", "image_filename": "steak_meal.jpg", "phone_number": "777-888-9999", "opening_hours": "Tue-Sun: 4pm-11pm", "website": "https://www.steakhouse.com"},
        {"name": "Seafood Shack", "owner_username": "jamesjohnson", "description": "Fresh seafood and coastal cuisine.", "rating": 4, "food_type": "Seafood", "location": "246 Ocean Dr", "image_filename": "seafood_meal.jpg", "phone_number": "222-333-4444", "opening_hours": "Mon-Sun: 11am-10pm", "website": "https://www.seafoodshack.com"},
        {"name": "Thai Terrace", "owner_username": "sophiebrown", "description": "Authentic Thai dishes and flavorful curries.", "rating": 5, "food_type": "Thai", "location": "135 Sunset Ave", "image_filename": "tai_place.jpg", "phone_number": "555-666-7777", "opening_hours": "Tue-Sun: 12pm-3pm, 5pm-10pm", "website": "https://www.thaiterrace.com"},
        {"name": "Greek Grill", "owner_username": "williamsmith", "description": "Traditional Greek recipes and Mediterranean flavors.", "rating": 4, "food_type": "Greek", "location": "864 Olive St", "image_filename": "greek_place.jpg", "phone_number": "888-999-1111", "opening_hours": "Mon-Sat: 11am-10pm", "website": "https://www.greekgrill.com"},
        {"name": "Vegan Vibes", "owner_username": "oliverjones", "description": "Plant-based meals and healthy options.", "rating": 5, "food_type": "Vegan", "location": "579 Vine Rd", "image_filename": "vegan_place.jpg", "phone_number": "999-111-2222", "opening_hours": "Mon-Fri: 10am-8pm, Sat-Sun: 10am-6pm", "website": "https://www.veganvibes.com"},
    ]

    restaurants = {rd["name"]: add_restaurant(**rd, users=users) for rd in restaurant_data}

    # Reviews
    review_data = [
        {"text": "Amazing pizza! The crust was perfectly crispy.", "rating": 5, "restaurant_name": "The Pizza Place", "reviewer_username": "issacnewton"},
        {"text": "Great burgers and friendly service.", "rating": 4, "restaurant_name": "Burger Joint", "reviewer_username": "galileogalilei"},
        {"text": "The sushi was so fresh and delicious.", "rating": 5, "restaurant_name": "Sushi Spot", "reviewer_username": "alberteinstein"},
        {"text": "Authentic Mexican flavors. The tacos were outstanding.", "rating": 4, "restaurant_name": "Taco City", "reviewer_username": "mariamcurie"},
        {"text": "The pasta dishes were homemade and tasty.", "rating": 4, "restaurant_name": "Pasta Palace", "reviewer_username": "charlesdarwin"},
        {"text": "The steak was cooked to perfection. Highly recommended.", "rating": 5, "restaurant_name": "Steak House", "reviewer_username": "issacnewton"},
        {"text": "Fresh seafood and great coastal ambiance.", "rating": 4, "restaurant_name": "Seafood Shack", "reviewer_username": "galileogalilei"},
        {"text": "The Thai curries were flavorful and spicy. Loved it!", "rating": 5, "restaurant_name": "Thai Terrace", "reviewer_username": "alberteinstein"},
        {"text": "Authentic Greek flavors. The gyros were delicious.", "rating": 4, "restaurant_name": "Greek Grill", "reviewer_username": "mariamcurie"},
        {"text": "Fantastic vegan options. The plant-based burgers were amazing.", "rating": 5, "restaurant_name": "Vegan Vibes", "reviewer_username": "charlesdarwin"},
        {"text": "Decent pizza, but I've had better.", "rating": 3, "restaurant_name": "The Pizza Place", "reviewer_username": "galileogalilei"},
        {"text": "The burgers were a bit dry, but the fries were good.", "rating": 3, "restaurant_name": "Burger Joint", "reviewer_username": "alberteinstein"},
        {"text": "Average sushi. Nothing extraordinary.", "rating": 3, "restaurant_name": "Sushi Spot", "reviewer_username": "mariamcurie"},
        {"text": "The tacos were okay, but not the best I've had.", "rating": 3, "restaurant_name": "Taco City", "reviewer_username": "charlesdarwin"},
        {"text": "The pasta was overcooked and lacked flavor.", "rating": 2, "restaurant_name": "Pasta Palace", "reviewer_username": "issacnewton"},
        {"text": "The steak was tough and not worth the price.", "rating": 2, "restaurant_name": "Steak House", "reviewer_username": "galileogalilei"},
        {"text": "Disappointing seafood. Not fresh and overpriced.", "rating": 2, "restaurant_name": "Seafood Shack", "reviewer_username": "alberteinstein"},
        {"text": "The Thai food was too sweet and not authentic.", "rating": 2, "restaurant_name": "Thai Terrace", "reviewer_username": "mariamcurie"},
        {"text": "The Greek dishes were bland and uninspired.", "rating": 2, "restaurant_name": "Greek Grill", "reviewer_username": "charlesdarwin"},
        {"text": "Limited vegan options. The dishes lacked creativity.", "rating": 2, "restaurant_name": "Vegan Vibes", "reviewer_username": "issacnewton"},
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

def add_restaurant(name, owner_username, description, rating, food_type, location, phone_number, opening_hours, website, users, image_filename):
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
            'phone_number': phone_number,
            'opening_hours': opening_hours,
            'website': website,
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