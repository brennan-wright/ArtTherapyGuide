from django.contrib import admin

from directive.forms import (DirectiveImageFormSet,
                             DirectiveInstructionFormSet,
                             DirectiveMaterialFormSet,
                             DirectiveObjectiveFormSet)
from directive.models import (DirectiveImage, DirectiveInstruction,
                              DirectiveMaterial, DirectiveObjective,
                              DirectivePage, DirectivePopulation,
                              DirectiveTheme)


@admin.register(DirectiveTheme)
class DirectiveThemeAdmin(admin.ModelAdmin):
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


class DirectivImageAdmin(admin.TabularInline):
    model = DirectiveImage
    formset = DirectiveImageFormSet


@admin.register(DirectivePage)
class DirectivePageAdmin(admin.ModelAdmin):
    list_display = ("title", "posted_by", "created")
    list_filter = ("posted_by", "created", "updated",
                   "theme", "population")
    search_fields = ("title",)
    inlines = [DirectiveObjectiveAdmin,
               DirectiveMaterialAdmin, DirectivInstructionAdmin, DirectivImageAdmin]
