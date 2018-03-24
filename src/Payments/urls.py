from django.conf.urls import url
from . import views

app_name = "Payments"

urlpatterns = [
    url(r'^pay/$', views.PaymentViews,name="payment"),
    url(r'^user/pay/$', views.PaidUserViews,name="user_pay"),
    
]
