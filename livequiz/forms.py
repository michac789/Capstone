from django import forms
from django.utils.safestring import mark_safe


class GameForm(forms.Form):
    title = forms.CharField(label = mark_safe("Title"), max_length = 64,
                            widget = forms.TextInput(attrs = {"class": 'form_title',}))
    description = forms.CharField(widget = forms.Textarea(attrs = {
        'placeholder': "Enter description here...", "class": "form_description",
    }), max_length = 256)
    
    
