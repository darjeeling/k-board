from django import forms
from board.models import Post

class PostForm(forms.models.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', )
