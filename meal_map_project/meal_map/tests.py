import os
from django.test import TestCase
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from meal_map_project import settings
from meal_map.models import Restaurant, RestaurantOwner, Review, Reviewer
from populate_meal_map import add_user, add_restaurant

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class UserLoginTestCase(TestCase):
    def setUp(self):
        # Set up test users haha
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.inactive_user = User.objects.create_user(username='inactiveuser', password='testpass123', is_active=False)

    def test_login_successful(self):
        # Test successful login
        response = self.client.post(reverse('meal_map:login'), {'username': 'testuser', 'password': 'testpass123'})
        self.assertRedirects(response, reverse('meal_map:homepage'))
        
    def test_login_get_request(self):
        # Test accessing login page via GET request
        response = self.client.get(reverse('meal_map:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meal_map/login.html')


class StructureTests(TestCase):
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.meal_map_app_dir = os.path.join(self.project_base_dir, 'meal_map')
    
    def test_project_created(self):
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'meal_map_project'))
        urls_module_exists = os.path.isfile(os.path.join(self.project_base_dir, 'meal_map_project', 'urls.py'))
        
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your meal_map_project configuration directory doesn't seem to exist. Did you use the correct name?{FAILURE_FOOTER}")
        self.assertTrue(urls_module_exists, f"{FAILURE_HEADER}Your project's urls.py module does not exist. Did you use the startproject command?{FAILURE_FOOTER}")
    
    def test_meal_map_app_created(self):
        directory_exists = os.path.isdir(self.meal_map_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.meal_map_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.meal_map_app_dir, 'views.py'))
        
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The meal_map app directory does not exist. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(is_python_package, f"{FAILURE_HEADER}The meal_map directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(views_module_exists, f"{FAILURE_HEADER}The meal_map directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")
    
    def test_meal_map_has_urls_module(self):
        module_exists = os.path.isfile(os.path.join(self.meal_map_app_dir, 'urls.py'))
        self.assertTrue(module_exists, f"{FAILURE_HEADER}The meal map app's urls.py module is missing. Read over the instructions carefully, and try again. You need TWO urls.py modules.{FAILURE_FOOTER}")
    
    def test_is_meal_map_app_configured(self):
        is_app_configured = 'meal_map' in settings.INSTALLED_APPS
        self.assertTrue(is_app_configured, f"{FAILURE_HEADER}The meal map app is missing from your setting's INSTALLED_APPS list.{FAILURE_FOOTER}")


class TemplatesStructureTests(TestCase):
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.meal_map_templates_dir = os.path.join(self.templates_dir, 'meal_map')
    
    def test_templates_directory_exists(self):
        directory_exists = os.path.isdir(self.templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your project's templates directory does not exist.{FAILURE_FOOTER}")
    
    def test_meal_map_templates_directory_exists(self):
        directory_exists = os.path.isdir(self.meal_map_templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The Meal Map templates directory does not exist.{FAILURE_FOOTER}")
    
    def test_template_dir_setting(self):
        variable_exists = 'TEMPLATE_DIR' in dir(settings)
        self.assertTrue(variable_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable TEMPLATE_DIR defined!{FAILURE_FOOTER}")
        
        template_dir_value = os.path.normpath(settings.TEMPLATE_DIR)
        template_dir_computed = os.path.normpath(self.templates_dir)
        self.assertEqual(template_dir_value, template_dir_computed, f"{FAILURE_HEADER}Your TEMPLATE_DIR setting does not point to the expected path. Check your configuration, and try again.{FAILURE_FOOTER}")
    
    def test_template_lookup_path(self):
        lookup_list = settings.TEMPLATES[0]['DIRS']
        found_path = False
        
        for entry in lookup_list:
            entry_normalised = os.path.normpath(entry)
            
            if entry_normalised == os.path.normpath(settings.TEMPLATE_DIR):
                found_path = True
        
        self.assertTrue(found_path, f"{FAILURE_HEADER}Your project's templates directory is not listed in the TEMPLATES>DIRS lookup list. Check your settings.py module.{FAILURE_FOOTER}")
    
    def test_templates_exist(self):
        base_path = os.path.join(self.meal_map_templates_dir, 'base.html')
        homepage_path = os.path.join(self.meal_map_templates_dir, 'homepage.html')
        
        self.assertTrue(os.path.isfile(base_path), f"{FAILURE_HEADER}Your base.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(homepage_path), f"{FAILURE_HEADER}Your homepage.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")


class BasePageTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('meal_map:base'))
    
    def test_homepage_uses_template(self):
        self.assertTemplateUsed(self.response, 'meal_map/base.html', f"{FAILURE_HEADER}Your base() view does not use the expected index.html template.{FAILURE_FOOTER}")
    
    def test_homepage_starts_with_doctype(self):
        self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{FAILURE_HEADER}Your base.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FAILURE_FOOTER}")
    

class StaticMediaTests(TestCase):
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.static_dir = os.path.join(self.project_base_dir, 'static')
        self.media_dir = os.path.join(self.project_base_dir, 'media')
    
    def test_does_static_directory_exist(self):
        """
        Tests whether the static directory exists in the correct location -- and the images subdirectory.
        Also checks for the presence of rango.jpg in the images subdirectory.
        """
        does_static_dir_exist = os.path.isdir(self.static_dir)
        does_images_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'images'))
        does_logo_jpeg_exist = os.path.isfile(os.path.join(self.static_dir, 'images', 'logo.jpeg'))
        does_default_jpg_exist = os.path.isfile(os.path.join(self.static_dir, 'images', 'default-profile.jpg'))
        
        self.assertTrue(does_static_dir_exist, f"{FAILURE_HEADER}The static directory was not found in the expected location. Check the instructions in the book, and try again.{FAILURE_FOOTER}")
        self.assertTrue(does_images_static_dir_exist, f"{FAILURE_HEADER}The images subdirectory was not found in your static directory.{FAILURE_FOOTER}")
        self.assertTrue(does_logo_jpeg_exist, f"{FAILURE_HEADER}We couldn't locate the logo.jpg image in the /static/images/ directory. If you think you've included the file, make sure to check the file extension. Sometimes, a JPG can have the extension .jpeg. Be careful! It must be .jpg for this test.{FAILURE_FOOTER}")
        self.assertTrue(does_default_jpg_exist, f"{FAILURE_HEADER}We couldn't locate the default-profile.jpg image in the /static/images/ directory. If you think you've included the file, make sure to check the file extension. Sometimes, a JPG can have the extension .jpeg. Be careful! It must be .jpg for this test.{FAILURE_FOOTER}")
    
    def test_does_media_directory_exist(self):
        does_media_dir_exist = os.path.isdir(self.media_dir)
        self.assertTrue(does_media_dir_exist, f"{FAILURE_HEADER}We couldn't find the /media/ directory in the expected location. Make sure it is in your project directory (at the same level as the manage.py module).{FAILURE_FOOTER}")
    
    def test_static_and_media_configuration(self):
        static_dir_exists = 'STATIC_DIR' in dir(settings)
        self.assertTrue(static_dir_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable STATIC_DIR defined.{FAILURE_FOOTER}")
        
        expected_path = os.path.normpath(self.static_dir)
        static_path = os.path.normpath(settings.STATIC_DIR)
        self.assertEqual(expected_path, static_path, f"{FAILURE_HEADER}The value of STATIC_DIR does not equal the expected path. It should point to your project root, with 'static' appended to the end of that.{FAILURE_FOOTER}")
        
        staticfiles_dirs_exists = 'STATICFILES_DIRS' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, f"{FAILURE_HEADER}The required setting STATICFILES_DIRS is not present in your project's settings.py module. Check your settings carefully. So many students have mistyped this one.{FAILURE_FOOTER}")
        self.assertEqual([static_path], settings.STATICFILES_DIRS, f"{FAILURE_HEADER}Your STATICFILES_DIRS setting does not match what is expected. Check your implementation against the instructions provided.{FAILURE_FOOTER}")
        
        staticfiles_dirs_exists = 'STATIC_URL' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, f"{FAILURE_HEADER}The STATIC_URL variable has not been defined in settings.py.{FAILURE_FOOTER}")
        self.assertEqual('/static/', settings.STATIC_URL, f"{FAILURE_HEADER}STATIC_URL does not meet the expected value of /static/. Make sure you have a slash at the end!{FAILURE_FOOTER}")
        
        media_dir_exists = 'MEDIA_DIR' in dir(settings)
        self.assertTrue(media_dir_exists, f"{FAILURE_HEADER}The MEDIA_DIR variable in settings.py has not been defined.{FAILURE_FOOTER}")
        
        expected_path = os.path.normpath(self.media_dir)
        media_path = os.path.normpath(settings.MEDIA_DIR)
        self.assertEqual(expected_path, media_path, f"{FAILURE_HEADER}The MEDIA_DIR setting does not point to the correct path. Remember, it should have an absolute reference to tango_with_django_project/media/.{FAILURE_FOOTER}")
        
        media_root_exists = 'MEDIA_ROOT' in dir(settings)
        self.assertTrue(media_root_exists, f"{FAILURE_HEADER}The MEDIA_ROOT setting has not been defined.{FAILURE_FOOTER}")
        
        media_root_path = os.path.normpath(settings.MEDIA_ROOT)
        self.assertEqual(media_path, media_root_path, f"{FAILURE_HEADER}The value of MEDIA_ROOT does not equal the value of MEDIA_DIR.{FAILURE_FOOTER}")
        
        media_url_exists = 'MEDIA_URL' in dir(settings)
        self.assertTrue(media_url_exists, f"{FAILURE_HEADER}The setting MEDIA_URL has not been defined in settings.py.{FAILURE_FOOTER}")
        
        media_url_value = settings.MEDIA_URL
        self.assertEqual('/media/', media_url_value, f"{FAILURE_HEADER}Your value of the MEDIA_URL setting does not equal /media/. Check your settings!{FAILURE_FOOTER}")
    
    def test_context_processor_addition(self):
        context_processors_list = settings.TEMPLATES[0]['OPTIONS']['context_processors']
        self.assertTrue('django.template.context_processors.media' in context_processors_list, f"{FAILURE_HEADER}The 'django.template.context_processors.media' context processor was not included. Check your settings.py module.{FAILURE_FOOTER}")
        

class DatabaseConfigurationTests(TestCase):
    def setUp(self):
        pass
    
    def does_gitignore_include_database(self, path):
        f = open(path, 'r')
        
        for line in f:
            line = line.strip()
            
            if line.startswith('db.sqlite3'):
                return True
        
        f.close()
        return False
    
    def test_databases_variable_exists(self):

        self.assertTrue(settings.DATABASES, f"{FAILURE_HEADER}Your project's settings module does not have a DATABASES variable, which is required.{FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAILURE_HEADER}You do not have a 'default' database configuration in your project's DATABASES configuration variable.{FAILURE_FOOTER}")


class RestaurantModelTestCase(TestCase):
    def setUp(self):
        # Set up a user and a restaurant owner
        user = User.objects.create_user(username='owneruser', password='testpass123')
        self.owner = RestaurantOwner.objects.create(user=user)

        # Set up a restaurant
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            description="A test description",
            phone_number="1234567890",
            opening_hours="9 AM - 9 PM",
            website="http://testrestaurant.com",
            food_type="Italian",
            location="Test Location",
            owner=self.owner,
        )

    def test_calculate_rating_no_reviews(self):
        # Test calculate_rating method when there are no reviews
        self.assertEqual(self.restaurant.calculate_rating(), 0.0, "Expected rating to be 0.0")

    def test_calculate_rating_with_reviews(self):
        reviewer_username = "testreviewer"
        reviewer_email = "testreviewer@example.com"
        reviewer_password = "password"
        reviewer_user = add_user(reviewer_username, reviewer_email, reviewer_password)
        reviewer = Reviewer.objects.create(user=reviewer_user)
        # Add reviews and test calculate_rating method
        Review.objects.create(restaurant=self.restaurant, rating=4, review_text="Good", reviewer=reviewer, date="2012-09-04 06:00")
        Review.objects.create(restaurant=self.restaurant, rating=5, review_text="Excellent", reviewer=reviewer, date="2012-09-04 06:00")
        self.assertEqual(self.restaurant.calculate_rating(), 4.5, "Expected rating to be 4.5")

    def test_slug_generation_on_save(self):
        # Test if slug is generated based on the restaurant's name
        expected_slug = slugify(self.restaurant.name)
        self.restaurant.save()  # Trigger save to ensure slug is generated
        self.assertEqual(self.restaurant.slug, expected_slug, f"Expected slug to be '{expected_slug}'")

    def test_str_representation(self):
        # Test the __str__ method
        self.assertEqual(str(self.restaurant), "Test Restaurant", "Expected string representation to be 'Test Restaurant'")


class AdminInterfaceTests(TestCase):
    def setUp(self):
        User.objects.create_superuser('testAdmin', 'email@email.com', 'adminPassword123')
        self.client.login(username='testAdmin', password='adminPassword123')
    
    def test_admin_interface_accessible(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}The admin interface is not accessible. Check that you didn't delete the 'admin/' URL pattern in your project's urls.py module.{FAILURE_FOOTER}")
    

class PopulateScriptTestCase(TestCase):
    def test_add_user(self):
        # Test the add_user function
        username = "testuser"
        email = "testuser@example.com"
        password = "password"
        user = add_user(username, email, password)
        self.assertIsInstance(user, User, "The user should be an instance of the User model")
        self.assertTrue(User.objects.filter(username=username).exists(), "The user should exist in the database")
        
    def test_add_restaurant(self):
        # Test the add_restaurant function
        user = User.objects.create_user(username='owneruser', password='testpass123')
        owner_username = user.username
        name = "Test Restaurant"
        description = "A test description"
        rating = 4
        food_type = "Italian"
        location = "Test Location"
        phone_number = "1234567890"
        opening_hours = "9 AM - 9 PM"
        website = "http://testrestaurant.com"
        users = {owner_username: user}
        image_filename = None  # Assume no image for simplicity
        
        restaurant = add_restaurant(name, owner_username, description, rating, food_type, location, phone_number, opening_hours, website, users, image_filename)
        self.assertIsInstance(restaurant, Restaurant, "The restaurant should be an instance of the Restaurant model")
        self.assertTrue(Restaurant.objects.filter(name=name).exists(), "The restaurant should exist in the database")
        
    def test_add_review(self):
        # Test the add_review function
        # First, create necessary objects (user, restaurant)
        reviewer_username = "testreviewer"
        reviewer_email = "testreviewer@example.com"
        reviewer_password = "password"
        reviewer_user = add_user(reviewer_username, reviewer_email, reviewer_password)
        reviewer, _ = Reviewer.objects.get_or_create(user=reviewer_user)
        
        owner_user = add_user("owneruser", "owneruser@example.com", "testpass123")
        owner = RestaurantOwner.objects.create(user=owner_user)
        restaurant = Restaurant.objects.create(name="Test Restaurant", owner=owner)
        
        text = "A test review"
        rating = 5

        review, _ = Review.objects.get_or_create(reviewer=reviewer, date="2012-09-04 06:00", review_text=text, rating=rating, restaurant=restaurant)
        self.assertIsInstance(review, Review, "The review should be an instance of the Review model")
        self.assertTrue(Review.objects.filter(review_text=text).exists(), "The review should exist in the database")


class MyReviewsViewTests(TestCase):
    def setUp(self):
        # Create a user and reviewer
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.reviewer = Reviewer.objects.create(user=self.user)
        owner_user = add_user("owneruser", "owneruser@example.com", "testpass123")
        owner = RestaurantOwner.objects.create(user=owner_user)
        restaurant = Restaurant.objects.create(name="Test Restaurant", owner=owner)
        
        # Create reviews
        self.review1 = Review.objects.create(reviewer=self.reviewer, review_text='Review 1', rating=5, restaurant=restaurant, date="2012-09-04 06:00")
        self.review2 = Review.objects.create(reviewer=self.reviewer, review_text='Review 2', rating=4, restaurant=restaurant, date="2012-09-04 06:00")

    def test_view_with_reviews(self):
        # Log the user in
        self.client.login(username='testuser', password='12345')
        
        # Access the my_reviews page
        response = self.client.get(reverse('meal_map:my_reviews'))
        
        # Check if the page is accessible and the correct template is used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meal_map/my_reviews.html')
        
        # Check if the context contains the user's reviews
        self.assertIn('all_reviews', response.context)
        self.assertEqual(len(response.context['all_reviews']), 2)

    def test_view_no_reviews(self):
        # Create a user without reviews
        user_no_reviews = User.objects.create_user(username='testuser2', password='54321')
        Reviewer.objects.create(user=user_no_reviews)
        
        # Log the new user in
        self.client.login(username='testuser2', password='54321')
        
        # Access the my_reviews page
        response = self.client.get(reverse('meal_map:my_reviews'))
        
        # Check if the context contains no reviews
        self.assertIn('all_reviews', response.context)
        self.assertEqual(len(response.context['all_reviews']), 0)

    def test_anonymous_user_redirect(self):
        # Access the my_reviews page without logging in
        response = self.client.get(reverse('meal_map:my_reviews'))
        
        # Check if the anonymous user is redirected to the login page
        self.assertEqual(response.status_code, 302) # or use assertRedirects for more detailed check

