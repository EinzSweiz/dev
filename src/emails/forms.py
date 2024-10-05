from django import forms
from .models import Email, EmailVerification
from .services import verify_email

from django import forms
from .services import verify_email

class EmailForm(forms.Form):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if verify_email(email=email):
            return email
        
        return email
