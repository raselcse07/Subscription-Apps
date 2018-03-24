from django.contrib.auth import get_user_model
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages
from .forms import PaymentForm,PaidUserForm
from .models import Transactions


User = get_user_model()


def PaymentViews(request):

	form=PaymentForm(request.POST or None)

	if form.is_valid():

		instance = form.save(commit=False)
		instance.save()
		qs = Transactions.objects.all().order_by('-id')[0]
		messages.info(request,"Payment successfully received")
		return render (request,"Payments/payment_info.html",{"qs":qs})

	template_name = "Payments/payment.html"
	context={

			"form":form,
	}

	return render(request,template_name,context)


def PaidUserViews(request):

	form = PaidUserForm(request.POST or None)

	if form.is_valid():

		instance=form.save(commit=False)
		qs_TxID = Transactions.objects.filter(transaction_id=form.cleaned_data.get("TxID")).exists()
		qs_user = User.objects.filter(username=form.cleaned_data.get("user_name")).exists()

		if qs_TxID and qs_user:

			expired_TxID=Transactions.objects.get(transaction_id=form.cleaned_data.get("TxID"))
			expired_TxID.expires=True
			expired_TxID.save()
			instance.save()
			messages.success(request,"Successfully Paid")
			return HttpResponseRedirect("/subscriber/login/")
		elif not qs_user:
			messages.info(request,"User does not exists.")
		elif not qs_TxID:
			messages.info(request,"Invalid TxID.")



	template_name = "Payments/paid_user.html"
	context={

			"form":form
	}


	return render(request,template_name,context)


