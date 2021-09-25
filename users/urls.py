from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/$', views.ProfileView, name='profile'),
    url(r'^delete-profile/$', views.UserDeleteView.as_view(), name='delete-profile'),
]
