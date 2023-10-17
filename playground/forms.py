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
        labels = {
            'username': 'Benutzername',
            'FavIce': 'Lieblingseis',
            'Shoesize': 'Hufgröße',
            'Age': 'Alter',
            'Hobbies': 'Deine Hobbies',
        }

        # Override password field labels and help text
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Passwort'
        self.fields['password1'].help_text = ' <br><br> Dein Passwort muss <li> mindestens 8 Zeichen haben, <li> aus Buchstaben und Zahlen bestehen <li> und darf nicht zu ähnlich zu deinen sonstigen Angaben sein'
        self.fields['password2'].label = 'Passwort bestätigen'
        self.fields['password2'].help_text = ''
