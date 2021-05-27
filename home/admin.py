from django.contrib import admin

from .models import AboutPage, ContactFormField, ContactPage, HomePage

# Register your models here.

admin.site.register(AboutPage)
admin.site.register(HomePage)
# Register your models here.

admin.site.register(ContactPage)
admin.site.register(ContactFormField)
