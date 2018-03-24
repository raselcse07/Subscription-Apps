from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,HttpResponseRedirect
from Payments.models import PaidUser,Transactions
from Subscriber.models import Profile
from .forms import ActivateUserForm




User=get_user_model()



# This views retrieves all user information

def AllUser(request):

	user_qs = User.objects.all()
	TxID_qs = PaidUser.objects.all()

	page = request.GET.get('page', 1)
	paginator1 = Paginator(user_qs, 5)
	paginator2 = Paginator(TxID_qs, 5)


	try:
		users = paginator1.page(page)
	except PageNotAnInteger:
		users = paginator1.page(1)
	except EmptyPage:
		users = paginator1.page(paginator1.num_pages)
		
	try:
	
		TxID = paginator2.page(page)
	except PageNotAnInteger:
		
		TxID = paginator2.page(1)
	except EmptyPage:
		
		TxID = paginator2.page(paginator2.num_pages)



	template_name = "PaymentChecker/users.html"
	context={

			"TxID":TxID,
			"users":users
	}

	return render(request,template_name,context)


# This views retrieves a specific inactive user

def ActivateUser(request,username=None):


	qs=User.objects.get(username=username)
	form=ActivateUserForm(request.POST or None,instance=qs)
	TxIDinfo=PaidUser.objects.get(user_name=qs)
	checkExp=Transactions.objects.get(transaction_id=TxIDinfo.TxID) 

	if form.is_valid() and "activate" in request.POST:

		user_profile = Profile()
		user_profile.user=qs
		user_profile.email=qs.email
		user_profile.billing_cycle=checkExp.billing_cycle
		user_profile.expiry_date=user_profile.subscription_date + timedelta(days=360)
		user_profile.save()
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect("/paymentchecker/all_users/")

	if form.is_valid() and "reject" in request.POST:

		qs.delete()
		
		return HttpResponseRedirect("/paymentchecker/all_users/")

	template_name = "PaymentChecker/users_activate.html"
	context={

			"form":form,
			"qs":qs,
			"checkExp":checkExp
	}

	return render(request,template_name,context)