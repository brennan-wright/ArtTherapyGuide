from django.contrib import admin

from directive.forms import (DirectiveInstructionFormSet,
                             DirectiveMaterialFormSet,
                             DirectiveObjectiveFormSet)
from directive.models import (DirectiveDiagnosis, DirectiveImage,
                              DirectiveInstruction, DirectiveMaterial,
                              DirectiveObjective, DirectivePage,
                              DirectivePopulation)


@admin.register(DirectiveDiagnosis)
class DirectiveDiagnosisAdmin(admin.ModelAdmin):
    pass


@admin.register(DirectiveImage)
class DirectiveImageAdmin(admin.ModelAdmin):
    pass


@admin.register(DirectivePopulation)
class DirectivePopulationAdmin(admin.ModelAdmin):
    pass


class DirectiveObjectiveAdmin(admin.TabularInline):
    model = DirectiveObjective
    formset = DirectiveObjectiveFormSet


class DirectiveMaterialAdmin(admin.TabularInline):
    model = DirectiveMaterial
    formset = DirectiveMaterialFormSet


class DirectivInstructionAdmin(admin.TabularInline):
    model = DirectiveInstruction
    formset = DirectiveInstructionFormSet


@admin.register(DirectivePage)
class DirectivePageAdmin(admin.ModelAdmin):
    list_display = ("title", "posted_by", "created")
    list_filter = ("posted_by", "created", "updated",
                   "diagnosis", "population")
    search_fields = ("title",)
    inlines = [DirectiveObjectiveAdmin,
               DirectiveMaterialAdmin, DirectivInstructionAdmin]
