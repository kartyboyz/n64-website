from django import forms

class QueryForm(forms.Form):
    Elements = forms.CharField(required=False)
    Conditions = forms.CharField(required=False)

class VideoForm(forms.Form):
    event = forms.CharField(required=False)
    race = forms.CharField(required=False)
    player = forms.CharField(required=False)
