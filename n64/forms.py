from django import forms

class QueryForm(forms.Form):
    Output_Columns = forms.CharField(required=False)
    Filters = forms.CharField(required=False)

class WatchForm(forms.Form):
    videoNum = forms.IntegerField()
