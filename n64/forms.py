from django import forms

class BoxQueryForm(forms.Form):
    Events = forms.CharField()

class TextQueryForm(forms.Form):
    Output_text = forms.CharField(required=False)
    Filter_text = forms.CharField(required=False)

class WatchForm(forms.Form):
    video_id = forms.IntegerField()
