from datetime import datetime, timedelta
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save







class Profile(models.Model):

	user					= models.CharField(max_length=200)
	email 					= models.CharField(max_length=200)
	first_name  			= models.CharField(max_length=200)
	last_name 				= models.CharField(max_length=200)
	subscription_date		= models.DateTimeField(default=timezone.now())
	expiry_date 			= models.DateTimeField()
	billing_cycle 			= models.CharField(max_length=200)


	def __str__(self):

		return self.user


	def get_absolute_url(self):

		return reverse("Subscriber:subscriber_profile", kwargs={"user": self.user})


	@property
	def is_expire(self):

		if timezone.now() >= self.expiry_date:
			return True
		return False

	@property
	def days_left(self):
		return self.expiry_date - timezone.now()

	@property
	def get_full_name(self):

		return self.first_name + " " + self.last_name


