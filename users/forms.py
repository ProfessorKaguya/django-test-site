from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(label="Имя пользователя", required=True)
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileImageForm(forms.ModelForm):
    img = forms.ImageField(label='Загрузить фото', required=False, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['img']

class ProfileSexForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['sex']
        widgets = {
            'sex': forms.Select,
        }
class ProfileAgreedForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['agreed']
        widgets = {
            'agreed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'agreed': 'Согласие на получение уведомлений на почту',
        }