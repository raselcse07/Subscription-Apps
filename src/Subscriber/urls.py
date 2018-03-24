from django.conf.urls import url
from . import views

app_name="Subscriber"

urlpatterns = [
    url(r'^register/$', views.SubscriberRegistration,name="register"),
    url(r'^login/$', views.SubscriberLogin,name="login"),
    url(r'^logout/$', views.UserLogout,name="logout"),
    url(r'^pay/$', views.SubscriptionPayment,name="pay"),
    url(r'^(?P<user>[a-z0-9].*)/profile/$', views.ProfileView,name="subscriber_profile"),
    url(r'^(?P<user>[a-z0-9].*)/profile/edit/$', views.UpdateProfile,name="update_profile"),


]

