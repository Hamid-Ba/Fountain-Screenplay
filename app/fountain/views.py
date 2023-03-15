from rest_framework import viewsets , generics, views ,response ,status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404



# Create your views here.

from . import models
from . import serializers


class FrameViewSet(viewsets.ModelViewSet):
    queryset = models.Frame.objects.order_by("-id")
    serializer_class = serializers.FrameSerializer

class PackagesList(viewsets.ModelViewSet):
    queryset = models.Package.objects.order_by("-id")
    serializer_class = serializers.PackageSerializer

class FountainViewSet(viewsets.ModelViewSet):
    queryset = models.Fountain.objects.all()
    serializer_class = serializers.FountainSerializer

class FountainSetMusic(generics.UpdateAPIView):
    queryset = models.Fountain.objects.all()
    serializer_class = serializers.FountainMusicSerializer