from django import forms
from captcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    email = forms.CharField(
        label='Your email address',
        widget=forms.EmailInput(attrs={
            'class': 'email'
        }))
    message = forms.CharField(
        label='How can we help?',
        widget=forms.Textarea(attrs={
            'class': 'message'
        }))
    captcha = ReCaptchaField(label='Are you a human?')
