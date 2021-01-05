from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)
