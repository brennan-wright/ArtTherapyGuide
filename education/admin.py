from django.contrib import admin

from education.models import EducationAudience, EducationPage, EducationRemote

# Register your models here.

admin.site.register(EducationAudience)

admin.site.register(EducationRemote)


@admin.register(EducationPage)
class EducationPageAdmin(admin.ModelAdmin):
    # regular stuff
    list_display = ("school_name", "degree_offered", "posted_by")

    class Media:
        js = ('regions.js',)
