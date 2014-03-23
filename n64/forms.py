from django import forms

class QueryForm(forms.Form):
    event = forms.CharField(required=False)
    race = forms.CharField(required=False)
    player = forms.CharField(required=False)
