from django import forms
from django.utils.safestring import mark_safe


class GameForm(forms.Form):
    title = forms.CharField(label = mark_safe("Title"), max_length = 64,
                            widget = forms.TextInput(attrs = {
                                "class": 'form_title form-control',
                                }))
    description = forms.CharField(widget = forms.Textarea(attrs = {
        'placeholder': "Explain briefly what your game is about...",
        "class": "form_description form-control",
        'rows': 4,
    }), max_length = 256)


class CodeForm(forms.Form):
    sessioncode = forms.CharField(label = "Enter code", max_length = 6,
                                  widget = forms.TextInput(attrs = {
                                      "placeholder": "6-character code",
                                  }))


class AddQuesForm(forms.Form):
    ques_count = forms.IntegerField(label = "Add these amount of questions",
                                    min_value = 1, max_value = 10,
                                    initial = 1)
