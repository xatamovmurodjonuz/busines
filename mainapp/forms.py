from django import forms
from .models import Business, Comment

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'description', 'image', 'location']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
