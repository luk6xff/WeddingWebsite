from django import forms


class RsvpForm(forms.Form):
    name = forms.CharField(max_length=50)
    confirm_or_not = forms.RadioSelect(choices=("Confirm", "Reject"))
    send_email_with_info = forms.BooleanField()
    email = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea)

