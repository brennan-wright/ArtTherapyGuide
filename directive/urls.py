from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ListDirectivePage.as_view(), name='list_directive_post'),
    url(r'^detail/(?P<uuid>[-\w]*)/?$',
        views.DetailDirectivePage.as_view(), name='detail_directive_post'),
    url(r'^new/$', views.CreateDirectivePage.as_view(), name='new_directive_post'),
    url(r'^delete/(?P<uuid>[-\w]*)/?$',
        views.DeleteDirectivePage.as_view(), name='delete_directive_entry'),
    url(r'^edit/(?P<uuid>[-\w]*)/?$',
        views.EditDirectivePage.as_view(), name='edit_directive_post'),
    url(r'^thank-you/(?P<uuid>[-\w]*)/?$',
        views.ThanksPage.as_view(), name='thanks_directive_post')
]
