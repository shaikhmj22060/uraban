from django import forms
from .models import *


class categoryform (forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'image')
        