from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = "fountain"

router = DefaultRouter()

router.register("frame", views.FrameViewSet)

urlpatterns = [path("", include(router.urls))]
