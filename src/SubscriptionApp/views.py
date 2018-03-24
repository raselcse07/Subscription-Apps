from django.shortcuts import render




def Homepage(request):


	template_name  = "Homepage/index.html"
	context={


	}

	return render(request,template_name,context)