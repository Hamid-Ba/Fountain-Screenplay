from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = "fountain"

router = DefaultRouter()

router.register("frame", views.FrameViewSet)
router.register("fount", views.FountainViewSet)
router.register("package", views.PackagesList)

urlpatterns = [
    path("", include(router.urls)),
    path("set_music/<int:pk>", views.FountainSetMusic.as_view()),
    path("text/<int:fount_id>", views.TextOutputViewSet.as_view()),
]
