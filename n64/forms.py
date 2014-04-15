from django import forms

class QueryForm(forms.Form):
    Elements = forms.CharField(required=False)
    Conditions = forms.CharField(required=False)

class VideoForm(forms.Form):
    videoNum = forms.CharField(required=False)
