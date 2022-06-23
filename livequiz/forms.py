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


class AddQuesForm(forms.Form):
    ques_count = forms.IntegerField(label = "Add these amount of questions",
                                    min_value = 1, max_value = 10)

