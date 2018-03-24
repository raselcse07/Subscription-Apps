from django import forms
from .models import Transactions,PaidUser




class PaymentForm(forms.ModelForm):


	class Meta:
		model=Transactions
		fields=[
				"user_name",
				"billing_cycle"
				]

class PaidUserForm(forms.ModelForm):

	class Meta:

		model=PaidUser
		fields=["user_name","TxID"]