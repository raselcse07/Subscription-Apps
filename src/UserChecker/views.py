from django.contrib.auth import get_user_model
from django.shortcuts import render,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ActivateUserForm


User=get_user_model()



# This views retrieves all user information

def AllUser(request):

	user_qs = User.objects.all()

	page = request.GET.get('page', 1)
	paginator= Paginator(user_qs, 5)


	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
		
	

	template_name = "UserChecker/users.html"
	context={
			"users":users
	}

	return render(request,template_name,context)

# This views retrieves a specific inactive user

def ActivateUser(request,username=None):

	qs=User.objects.get(username=username)
	form=ActivateUserForm(request.POST or None,instance=qs)

	if form.is_valid() and "activate" in request.POST:

		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect("/users/all_user/")

	if form.is_valid() and "reject" in request.POST:

		qs.delete()
		
		return HttpResponseRedirect("/users/all_user/")

	template_name = "UserChecker/users_activate.html"
	context={

			"form":form,
			"qs":qs
	}

	return render(request,template_name,context)