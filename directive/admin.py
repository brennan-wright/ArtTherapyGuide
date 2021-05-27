from django.contrib import admin

from directive.models import (DirectiveAudience, DirectiveDiagnosis,
                              DirectiveImages, DirectivePage,
                              DirectivePopulation)

# Register your models here.


@admin.register(DirectiveAudience)
class DirectiveAudienceAdmin(admin.ModelAdmin):
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
    # regular stuff
    list_display = ("posted_by",)
