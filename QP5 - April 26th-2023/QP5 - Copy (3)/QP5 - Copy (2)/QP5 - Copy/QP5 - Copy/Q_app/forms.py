

# Importing forms module from django
from django import forms


# Define a form for forgot password functionality
class fpForm(forms.Form):
    # Defining fields for the form
    mail = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id':'password1'})) # Field for new password
    confirm_password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id':'password2'})) # Field for confirming new password
    # Using TextInput widget to hide password characters and setting id attribute for JS interaction
