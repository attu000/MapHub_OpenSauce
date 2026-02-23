from django import forms
from . import models


class SiteCreateForm(forms.ModelForm):
    class Meta:
        model = models.Site
        exclude = ('created_at', 'member')


class ContentCreateForm0(forms.ModelForm):#a title
    class Meta:
        model = models.Content
        fields = ['title']

class ContentCreateForm1(forms.ModelForm):#a text
    class Meta:
        model = models.Content
        fields = ['text1']

class ContentCreateForm2(forms.ModelForm):#a toguru
    class Meta:
        model = models.Content
        fields = ['title', 'text1']
