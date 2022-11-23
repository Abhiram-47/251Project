from django import forms

class createnew(forms.Form):
    name = forms.CharField(label="naama",max_length=200)
    check = forms.BooleanField(required= False)