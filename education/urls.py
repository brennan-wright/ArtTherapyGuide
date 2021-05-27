from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.ListEducationPage.as_view(), name='list_education_post'),
    url(r'^my-posts/$', views.ListUserEducationPage.as_view(),
        name='list_user_education_post'),
    url(r'^detail/(?P<uuid>[-\w]*)/?$',
        views.DetailEducationPage.as_view(), name='detail_education_post'),
    url(r'^new/$', views.CreateEducationPage.as_view(), name='new_education_post'),
    url(r'^delete/(?P<uuid>[-\w]*)/?$',
        views.DeleteEducationPage.as_view(), name='delete_education_entry'),
    url(r'^edit/(?P<uuid>[-\w]*)/?$',
        views.EditEducationPage.as_view(), name='edit_education_post'),
    url(r'^thank-you/(?P<uuid>[-\w]*)/?$',
        views.thanks, name='thanks_education_post'),
    path('ajax/load-cities/', views.load_cities,
         name='ajax_load_cities'),
]
