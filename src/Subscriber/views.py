from datetime import datetime, timedelta

from django.contrib.auth import (
								login,
								get_user_model,
								logout
								)

from django.contrib import messages
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from Accounts.forms import (
							UserCreationForm,
							UserLoginForm
							)

from Payments.models import Transactions,PaidUser
from .forms import SubscriptionPayForm,ProfileUpdateForm
from .models import Profile


User=get_user_model()

# This is Subscriber Registration Views

def SubscriberRegistration(request,*args,**kwargs):

	form=UserCreationForm(request.POST or None)

	if form.is_valid():

		instance= form.save(commit=False)
		instance.is_active=False
		instance.account_status=False
		instance.save()
		return HttpResponseRedirect("/payments/pay/")

	template_name="Subscriber/register.html"
	context={

			"form":form
	}

	return render(request,template_name,context)

# Subscriber Login views



def SubscriberLogin(request,*args,**kwargs):

	form=UserLoginForm(request.POST or None)
	user=""
	TxID=""
	Expires=""

	if form.is_valid():

			username_=form.cleaned_data.get("username")
			user_obj=User.objects.get(username__iexact=username_)

			if not user_obj.account_status:
				messages.info(request, 'Your approval status is pending using the information you submitted.')

			if user_obj.account_status:
				user=user_obj
				TxID_exists=PaidUser.objects.filter(user_name=user).exists()
				if TxID_exists:
					TxID=PaidUser.objects.get(user_name=user)
					Expires=Transactions.objects.get(transaction_id=TxID.TxID)

			if not user_obj.is_active:
				messages.info(request, 'Your account is not active yet.')
			else:
				login(request,user_obj)

				if not request.user.is_staff:
					profile=Profile.objects.get(user=user_obj)
					return HttpResponseRedirect(profile.get_absolute_url())


	template_name="Subscriber/login.html"
	context={

			"form":form,
			"user":user,
			"Expires":Expires
			}

	return render(request,template_name,context)


def SubscriptionPayment(request):

	form = SubscriptionPayForm(request.POST or None)

	if form.is_valid():

		TxID 	= form.cleaned_data.get("transaction_id")
		TxID_exists = Transactions.objects.get(transaction_id=TxID)
		if TxID_exists and TxID_exists.expires == False:

			try:
				user_ = Profile.objects.get(user=request.user.username)
				if user_:

					user_.billing_cycle = TxID_exists.billing_cycle
					user_.expiry_date = user_.subscription_date+timedelta(days=360)
					user_.save()
					TxID_exists.expires = True
					TxID_exists.save()
					return HttpResponseRedirect(user_.get_absolute_url())
					
			except:
				pass


		else:
			messages.info(request,"TxID expired")

	template_name = "Subscriber/subscription_pay.html"
	context={

				"form":form
			}

	return render(request,template_name,context)


def ProfileView(request,user=None):

	profile_obj=Profile.objects.get(user=user)
		
	template_name = "Subscriber/subscriber_profile.html"
	context={
				"profile_obj":profile_obj
			}

	return render(request,template_name,context)


def UpdateProfile(request,user=None):

	qs=Profile.objects.get(user=user)
	form =ProfileUpdateForm(request.POST or None,instance=qs)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(qs.get_absolute_url())
	template_name = "Subscriber/update_profile.html"
	context = {

			"form":form
	}

	return render(request,template_name,context)

def UserLogout(request):
	logout(request)
	return HttpResponseRedirect("/subscriber/login/")


