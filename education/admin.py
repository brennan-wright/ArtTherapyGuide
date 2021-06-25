from django.contrib import admin

from education.models import EducationLevel, EducationPage

# Register your models here.


admin.site.register(EducationLevel)


@admin.register(EducationPage)
class EducationPageAdmin(admin.ModelAdmin):
    # regular stuff
    list_display = ("school_name", "posted_by", "created")
    list_filter = ("posted_by", "created", "updated",
                   "education_level", "region",)
    search_fields = ("school_name",)

    class Media:
        js = ('regions.js',)
