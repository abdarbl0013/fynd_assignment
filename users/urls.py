from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.UserRegisterView.as_view()),
    url(r'^change_password/$', views.ChangePasswordView.as_view()),
    url(r'^details/$', views.UserDetailsView.as_view())
]
