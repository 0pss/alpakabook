from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


from django.contrib.auth.forms import UserCreationForm
from .models import User_dev2

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User_dev2  # Replace with your User_dev model
        fields = ['username', 'FavIce', 'Shoesize', 'Age', 'Hobbies']