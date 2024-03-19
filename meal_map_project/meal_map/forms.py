from django import forms
from django.contrib.auth.models import User
from meal_map.models import Restaurant, Review, Reviewer, RestaurantOwner

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
    
    def __init__(self, *args, **kwargs):
        self.reviewer = kwargs.pop('reviewer', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        review = super().save(commit=False)
        review.reviewer = self.reviewer
        if commit:
            review.save()
        return review    
    
        
class ReviewerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    profile_picture = forms.ImageField(widget=forms.FileInput(), required=False)
    
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "profile_picture"
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.set_password(user.password)
            user.save()
            reviewer = Reviewer.objects.create(user=user)
            reviewer.profile_picture = self.cleaned_data.get('profile_picture')
            reviewer.save()
        return user

class RestaurantOwnerForm(forms.ModelForm):
    restaurant_name = forms.CharField(max_length=128, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    profile_picture = forms.ImageField(widget=forms.FileInput(), required=False)
    
    class Meta:
        model = User
        fields = (
            "restaurant_name",
            "username",
            "email",
            "password",
            "profile_picture"
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.set_password(user.password)
            user.save()
            owner = RestaurantOwner.objects.create(user=user)
            owner.restaurant_name = self.cleaned_data.get('restaurant_name')
            owner.profile_picture = self.cleaned_data.get('profile_picture')
            owner.save()
        return user
