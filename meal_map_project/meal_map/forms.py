from django import forms
from django.contrib.auth.models import User
from meal_map.models import UserProfile, Restaurant, Review


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

class AddRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'description', 'phone_number', 'opening_hours', 
                  'website', 'rating', 'food_type', 'location', 'photo')
        
        widgets = {'name': forms.TextInput(attrs={'placeholder': 'Name of the Restaurant'}),
                   'description': forms.Textarea(attrs={'placeholder': 'Description'}),
                   'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number'}),
                   'opening_hours': forms.TextInput(attrs={'placeholder': 'Opening Hours'}),
                  'website': forms.URLInput(attrs={'placeholder': 'Website'}),
                  'rating': forms.HiddenInput,
                  'food_type': forms.TextInput(attrs={'placeholder': 'Food Type'}),
                  'location': forms.TextInput(attrs={'placeholder': 'Location'}),
                  'photo': forms.FileInput(),
                  }
        
class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'review_text')
        
        widgets = {'rating': forms.NumberInput(attrs={'placeholder': 'Rating out of 5'}),
                   'review_text': forms.Textarea(attrs={'placeholder': 'Tell us what you thought!'}),
                   }
        
        
    