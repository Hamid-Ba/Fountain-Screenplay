from django.contrib import admin
from .models import Frame
import datetime


class FrameAdmin(admin.ModelAdmin):
    """Frame Admin Model"""

    list_display = ("title","code", "type", "duration", "x_axis", "y_axis")
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


admin.site.register(Frame, FrameAdmin)
