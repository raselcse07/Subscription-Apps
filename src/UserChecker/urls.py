from django.conf.urls import url
from . import views


app_name="UserChecker"

urlpatterns = [
    url(r'^all_user/$', views.AllUser,name="user_list"),
    url(r'^(?P<username>[a-z0-9].*)/activate/$',views.ActivateUser,name="activate_user")

]
