from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^username/$', views.UserChangeUsernameView.as_view(), name='username'),
    url(r'^delete-profile/$', views.UserDeleteView.as_view(), name='delete-profile'),
]
