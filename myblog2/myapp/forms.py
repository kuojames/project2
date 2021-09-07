from django import forms
from myapp import models

class EmailPostFrom(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta: # 描述這張表單的情況
        model = models.Comment 
        fields = ('name','body')

class SearchForm(forms.Form):
    query = forms.CharField()        
