from django import forms

from secrets_share.models import Message


class SubmitForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='Message Text')
    password = forms.CharField(widget=forms.PasswordInput, label='Password (Optional)', required=False)

    class Meta:
        model = Message
        fields = ['text']