from django.conf.urls import url
from . import views 

app_name = "PaymentChecker"

urlpatterns = [

    url(r'^all_users/$', views.AllUser,name="all_users_payment_checker"),    
    url(r'^(?P<username>[a-z0-9].*)/activate/$',views.ActivateUser,name="activate_user_payment_checker")

]
