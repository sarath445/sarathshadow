from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Blogs, City
from django.contrib.auth import get_user_model
from django.forms import ModelForm, TextInput

class RegistrationForm(UserCreationForm):
    class Meta:
        model=get_user_model()
        fields =('username','email','phone',)

class UpdateForm(UserChangeForm):
    class Meta:
        model=get_user_model()
        fields=('phone','password')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password'].label=""
        self.fields['password'].help_text=""

class BlogForm(forms.ModelForm):
    class Meta:
        model=Blogs
        fields=('image','title','body')

class Cityform(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name' : TextInput(attrs={'class' :'input', 'placeholder' :'City Name'})}   