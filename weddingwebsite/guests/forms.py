from django import forms



PRESENCE_CONFIRMATION = (
    (0, 'No I will not attend you wedding party :('), 
    (1, 'Yes, I am going to celebrate your wedding with you :)')
)

HOTEL_CHOICES = (
    (0, 'Not interested'), 
    (1, 'Will stay in hotel')
)

class RsvpForm(forms.Form):
    name = forms.CharField(label='Your name:', max_length=50)
    presence_confirmation = forms.ChoiceField(label='Are you going to attend our wedding party?', choices=PRESENCE_CONFIRMATION, widget=forms.RadioSelect)
    hotel_needed = forms.ChoiceField(label='Do you want to stay in hotel?', choices=HOTEL_CHOICES)
    send_email_with_info = forms.BooleanField(label='Do you want to get an email with any update?')
    email = forms.EmailField(label='Your email:')
    comments = forms.CharField(label='Put you comments, questions below:', widget=forms.Textarea)

