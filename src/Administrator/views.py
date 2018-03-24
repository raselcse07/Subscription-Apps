from django.contrib.auth import get_user_model,login,logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,HttpResponseRedirect
from Subscriber.models import Profile
from .forms import ChekcerCreationForm

from Accounts.forms import UserLoginForm
							


User = get_user_model()


def AdminDashBoard(request):

	all_subscriber = Profile.objects.all()
	all_chekcer = User.objects.all()

	page = request.GET.get('page', 1)
	paginator1 = Paginator(all_subscriber, 10)
	paginator2 = Paginator(all_chekcer, 10)

	try:
		users = paginator1.page(page)
		checkers = paginator2.page(page)
	except PageNotAnInteger:
		users = paginator1.page(1)
		checkers = paginator2.page(1)
	except EmptyPage:
		users = paginator1.page(paginator1.num_pages)
		checkers = paginator2.page(paginator2.num_pages)

	template_name = "Administrator/dashboard.html"
	context = {

			"users":users,
			"checkers":checkers,
	}


	return render(request,template_name,context)


def CreateChecker(request):

	form = ChekcerCreationForm(request.POST or None)

	if form.is_valid():

		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect("/administrator/admin_area/")


	template_name = "Administrator/create_checker.html"
	context = {

			"form":form
	}


	return render(request,template_name,context)


def Login(request):

	form=UserLoginForm(request.POST or None)

	if form.is_valid():
		username_=form.cleaned_data.get("username")
		user_obj=User.objects.get(username__iexact=username_)
		login(request,user_obj)
		if request.user.is_admin:
			return HttpResponseRedirect("/administrator/admin_area/")
		if request.user.is_userchecker:
			return HttpResponseRedirect("/users/all_user/")
		if request.user.is_paymentchecker:
			return HttpResponseRedirect("/paymentchecker/all_users/")


	template_name = "Administrator/admin_login.html"
	context = {
				"form":form
			}

	return render(request,template_name,context)


def AdminLogout(request):
	logout(request)
	return HttpResponseRedirect("/")