from django import forms
from .models import Profile



class SubscriptionPayForm(forms.Form):

	transaction_id 		= forms.CharField()


class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model=Profile
		fields=['first_name','last_name']