
import debug_toolbar
from directive import urls as directive_urls
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from users import urls as users_urls

from . import views as health_check
from .views import AboutView, HomeView

urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt",
                             content_type="text/plain"),
    ),
    url(r'^health_check/', health_check.health_check.as_view()),
    url(r'^django-admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('accounts/', include('allauth.urls')),
    path('directives/', include(directive_urls)),
    path('about/',
         AboutView.as_view(), name='about'),
    path('',
         HomeView.as_view(), name='home'),
    path('user/', include(users_urls)),

]


if settings.DEBUG:
    from django.conf.urls.static import static

    # Serve static and media files from development server
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
