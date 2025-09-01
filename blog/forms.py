from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label="Your Comment")
