from django.conf.urls import url
from . import views

app_name = "Administrator"

urlpatterns = [

    url(r'^admin_area/$', views.AdminDashBoard,name="admin_area"),
    url(r'^add_new_checker/$', views.CreateChecker,name="checker_create"),
    url(r'^admin_login/$', views.Login,name="admin_login"),
    url(r'^admin_logout/$', views.AdminLogout,name="admin_logout"),

]
