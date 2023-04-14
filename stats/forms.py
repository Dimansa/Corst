from django import forms

class Years(forms.Form):
    first_date= forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control input-sm", "placeholder" : '2014'}))
    second_date= forms.CharField(widget=forms.TextInput(attrs={"class" : "form-control input-sm", "placeholder" : '2015'}))