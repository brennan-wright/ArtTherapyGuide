from django.contrib import admin

from directive.models import (DirectiveAudience, DirectiveDiagnosis,
                              DirectiveIdentifiedPatient, DirectivePage,
                              DirectivePopulation)


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


@admin.register(DirectivePage)
class DirectivePageAdmin(admin.ModelAdmin):
    list_display = ("title", "posted_by", "created")
    list_filter = ("posted_by", "created", "updated",
                   "audience", "diagnosis", "population")
    search_fields = ("title",)
