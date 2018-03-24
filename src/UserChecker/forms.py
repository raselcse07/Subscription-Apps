from django.contrib.auth import get_user_model
from django import forms


User=get_user_model()



class ActivateUserForm(forms.ModelForm):

	class Meta:

		model=User
		fields = ["account_status"]

