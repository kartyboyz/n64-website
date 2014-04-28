from django import forms

class BoxQueryForm(forms.Form):
    Events = forms.CharField()

class TextQueryForm(forms.Form):
    Outputs = forms.CharField(required=False)
    Filters = forms.CharField(required=False)

class WatchForm(forms.Form):
    video_id = forms.IntegerField()
