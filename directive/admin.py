from django.contrib import admin

from directive.models import (DirectiveAudience, DirectiveDiagnosis,
                              DirectiveIdentifiedPatient, DirectiveImages,
                              DirectivePage, DirectivePopulation)


@admin.register(DirectiveAudience)
class DirectiveAudienceAdmin(admin.ModelAdmin):
    pass


@admin.register(DirectiveIdentifiedPatient)
class DirectiveIdentifiedPatientAdmin(admin.ModelAdmin):
    pass


@admin.register(DirectiveDiagnosis)
class DirectiveDiagnosisAdmin(admin.ModelAdmin):
    pass


@admin.register(DirectivePopulation)
class DirectivePopulationAdmin(admin.ModelAdmin):
    pass


@admin.register(DirectiveImages)
class DirectiveImagesAdmin(admin.ModelAdmin):
    pass


class DirectiveImagesAdmin(admin.StackedInline):
    model = DirectiveImages
    extra = 3
    max_num = 3
    pass


@admin.register(DirectivePage)
class DirectivePageAdmin(admin.ModelAdmin):
    inlines = [DirectiveImagesAdmin]
    list_display = ("title", "posted_by", "created")
    list_filter = ("posted_by", "created", "updated",
                   "audience", "diagnosis", "population")
    search_fields = ("title", "directive_description")
