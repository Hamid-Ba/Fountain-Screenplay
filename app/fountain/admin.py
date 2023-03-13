from django.contrib import admin
from . import models
import datetime


class FrameAdmin(admin.ModelAdmin):
    """Frame Admin Model"""

    list_display = ("title", "code", "type", "duration", "x_axis", "y_axis")
    list_filter = ("type",)
    search_fields = ("title",)

    fieldsets = (
        (None, {"fields": ("title", "type", "orginal_image")}),
        (
            "Optional Fields",
            {"fields": ("analyzed_image", "duration", "x_axis", "y_axis")},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set duration on creation
            obj.duration = datetime.timedelta(minutes=5)
        super().save_model(request, obj, form, change)


class PackageAdmin(admin.ModelAdmin):
    list_display = ("order", "repeat", "frame")
    list_filter = ("frame",)
    search_fields = ("order", "repeat", "frame__title")


class FountainAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "title",
    )
    filter_horizontal = ("packages",)
    search_fields = ("title", "packages__order", "packages__frame__title")


admin.site.register(models.Frame, FrameAdmin)
admin.site.register(models.Package, PackageAdmin)
admin.site.register(models.Fountain, FountainAdmin)
