from django import forms


class DonationForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':"form-control"}))
    amount = forms.FloatField()
    message = forms.CharField(widget=forms.Textarea(), required=False)
    
