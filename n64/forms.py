from django import forms

class QueryForm(forms.Form):
    Outputs = forms.CharField(required=False)
    Filters = forms.CharField(required=False)

class WatchForm(forms.Form):
    videoNum = forms.IntegerField()
