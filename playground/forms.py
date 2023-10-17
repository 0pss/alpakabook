from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


from django.contrib.auth.forms import UserCreationForm
from .models import User_dev2


class CustomUserCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False, label='Profilbild')

    class Meta:
        model = User_dev2
        fields = ['username', 'FavIce', 'Shoesize', 'Age', 'Hobbies', 'profile_picture']
        labels = {
            'username': 'Benutzername',
            'FavIce': 'Lieblingseis',
            'Shoesize': 'Hufgröße',
            'Age': 'Alter',
            'Hobbies': 'Deine Hobbies',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Passwort'
        self.fields['password1'].help_text = 'Dein Passwort muss mindestens 8 Zeichen haben, aus Buchstaben und Zahlen bestehen und darf nicht zu ähnlich zu deinen sonstigen Angaben sein.'
        self.fields['password2'].label = 'Passwort bestätigen'
        self.fields['password2'].help_text = ''
