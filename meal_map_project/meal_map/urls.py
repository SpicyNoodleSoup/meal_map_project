from django.urls import path
from meal_map import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'meal_map'

urlpatterns = [
    
    path('restaurants/', views.RestaurantListView, name='restaurant-list'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView, name='restaurant-detail'),
    
    path('base/', views.base, name ='base'),
    path('register/', views.register, name ='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('homepage/', views.homepage, name='homepage'),
    path('my-account/', views.my_account, name ='my_account'),
    path('my-account/add-restaurant/', views.add_restaurant, name ='add_restaurant'),
    path('my-account/my-reviews/', views.my_reviews, name ='my_reviews'),
    path('restaurant/register/', views.restaurant_register, name='restaurant_register'),
    
    path('restaurant/<slug:restaurant_name_slug>', views.restaurant, name = 'show_restaurant')
]