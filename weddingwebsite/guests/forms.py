from django import forms
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe


PRESENCE_CONFIRMATION = (
    (1, _('Yes of course :)')),
    (0, _('No, unfortunately not :(')) 
)

HOTEL_CHOICES = (
    (0, _('No')), 
    (1, _('Yes'))
)

class RsvpGuestsNumForm(forms.Form):
    guests_num = forms.IntegerField(label=_('Number of guests you want to confirm/reject presence for:'), min_value=1, max_value=10)

class RsvpForm(forms.Form):

    def __init__(self, n,  *args, **kwargs):
        super(RsvpForm, self).__init__(*args, **kwargs)
        self.fields["name 0"] = forms.CharField(label=mark_safe("<strong> {} </strong>".format(_("Your name:"))), max_length=50)
        self.fields["presence_confirmation 0"] = forms.ChoiceField(label=_('Are you going to attend our wedding party?'), choices=PRESENCE_CONFIRMATION)
        self.fields["hotel_needed 0"] = forms.ChoiceField(label=_('Do you want to stay in hotel during the night?'), choices=HOTEL_CHOICES)
        for i in range(1,n):
            self.fields["name %d" % i] = forms.CharField(label=mark_safe("<strong> {} </strong>".format(_("Guest %(guest_id)s name:") % {'guest_id': i })), max_length=50)
            self.fields["presence_confirmation %d" % i] = forms.ChoiceField(label=_('Is he/she going to attend our wedding party?'), choices=PRESENCE_CONFIRMATION)
            self.fields["hotel_needed %d" % i] = forms.ChoiceField(label=_('Does he/she want to stay in hotel during the night?'), choices=HOTEL_CHOICES)
        
        self.fields["email"] = forms.EmailField(label=mark_safe("<strong> {} </strong>".format(_('If you wish to get some update info, leave us your email:'))), required=False)
        self.fields["comments"] = forms.CharField(label=mark_safe("<strong> {} </strong>".format(_('Put your comments, questions below:'))), required=False, widget=forms.Textarea)