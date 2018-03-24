from django.utils import timezone
from datetime import datetime, timedelta
from django.db import models
from django.db.models.signals import pre_save
from .utils import random_string_generator



BILLING_CYCLE=[

			("A","Plan A $100/year"),
			("B","Plan B $200/year"),
			("C","Plan C $300/year"),
			("D","Plan D $400/year")

]


class Transactions(models.Model):


	user_name 			= models.CharField(max_length=250,help_text="Fill it very carefully.")
	billing_cycle 		= models.CharField(max_length=200,choices=BILLING_CYCLE,default="A")
	transaction_id 		= models.CharField(max_length=200,unique=True)
	entry_date 			= models.DateTimeField(default=timezone.now())
	expires				= models.BooleanField(default=False)

	class Meta:

		verbose_name = "Transaction"
		verbose_name_plural= "Transaction"


	def __str__(self):

		return self.transaction_id

	


def trasaction_pre_save_receiver(sender,instance,*args,**kwargs):

	if not instance.transaction_id:
		instance.transaction_id=random_string_generator(size=6)		


pre_save.connect(trasaction_pre_save_receiver, sender=Transactions)




class PaidUser(models.Model):


	user_name 		= models.CharField(max_length=200)
	TxID 			= models.CharField(max_length=200,unique=True)



	def __str__(self):

		return self.TxID


	
