from django import forms
from myapp import models


# 直接以表單建立
class LoginForm(forms.Form):
    username = forms.CharField(label='ID', max_length=10)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class ProfileForm(forms.ModelForm): # ModelForm模型表單
    class Meta:
        model = models.Profile
        fields = ['height', 'male', 'website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['height'].label = '身高(cm)'
        self.fields['male'].label = '男性'
        self.fields['website'].label = '網站'





