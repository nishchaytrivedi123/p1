# forms.py
from django import forms
from .models import WeddingGuest, Family

class RSVPForm(forms.ModelForm):
    class Meta:
        model = WeddingGuest
        fields = ['first_name', 'last_name', 'email', 'rsvp_status', 'dietary_restrictions', 'message', 'is_rsvped']

# Form for Family model
class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['family_name', 'number_of_guests']

# Form for WeddingGuest model
class WeddingGuestForm(forms.ModelForm):
    class Meta:
        model = WeddingGuest
        fields = ['first_name', 'last_name', 'rsvp_status', 'dietary_restrictions', 'message', 'family']
        widgets = {
            'family': forms.Select(attrs={'required': False}),
        }

