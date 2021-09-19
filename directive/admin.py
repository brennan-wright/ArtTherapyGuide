from django.contrib import admin

from directive.forms import DirectiveObjectiveFormSet
from directive.models import (DirectiveDiagnosis, DirectiveObjective,
                              DirectivePage, DirectivePopulation)


@admin.register(DirectiveDiagnosis)
class DirectiveDiagnosisAdmin(admin.ModelAdmin):
    pass


@admin.register(DirectivePopulation)
class DirectivePopulationAdmin(admin.ModelAdmin):
    pass


class DirectiveObjectiveAdmin(admin.TabularInline):
    model = DirectiveObjective
    formset = DirectiveObjectiveFormSet


@admin.register(DirectivePage)
class DirectivePageAdmin(admin.ModelAdmin):
    list_display = ("title", "posted_by", "created")
    list_filter = ("posted_by", "created", "updated",
                   "diagnosis", "population")
    search_fields = ("title",)
    inlines = [DirectiveObjectiveAdmin, ]
