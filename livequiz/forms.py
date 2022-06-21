from django import forms
from django.utils.safestring import mark_safe

from .models import QuestionType1


class GameForm(forms.Form):
    title = forms.CharField(label = mark_safe("Title"), max_length = 64,
                            widget = forms.TextInput(attrs = {"class": 'form_title',}))
    description = forms.CharField(widget = forms.Textarea(attrs = {
        'placeholder': "Enter description here...", "class": "form_description",
    }), max_length = 256)


class CodeForm(forms.Form):
    sessioncode = forms.CharField(label = "Enter code", max_length = 6)


class QuestionForm(forms.Form):
    question = forms.CharField(label = "Question", max_length = 128)
    choice1 = forms.CharField(label = "Choice 1", max_length = 64)
    choice2 = forms.CharField(label = "Choice 2", max_length = 64)
    choice3 = forms.CharField(label = "Choice 3", max_length = 64)
    choice4 = forms.CharField(label = "Choice 4", max_length = 64)
    
    class Meta:
        model = QuestionType1
        fields = ["answer"] # BUGGY - TODO

