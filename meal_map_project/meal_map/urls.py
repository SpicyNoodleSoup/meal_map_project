from django.urls import path
from meal_map import views

app_name = 'meal_map'

urlpatterns = [
    
    path('restaurants/', views.RestaurantListView, name='restaurant-list'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView, name='restaurant-detail'),
    
    path('base/', views.base, name ='base'),
    path('login/', views.login, name='login'),
    path('homepage/', views.homepage, name='homepage'),
    path('my-account/', views.my_account, name ='my_account'),
    path('my-account/add-restaurant/', views.add_restaurant, name ='add_restaurant'),
    path('my-account/my-reviews/', views.my_reviews, name ='my_reviews'),
    path('register/', views.register, name ='register'),
    
    path('restaurant/<slug:restaurant_name_slug>', views.restaurant, name = 'show_restaurant')
    
    
   
    
    
    
]