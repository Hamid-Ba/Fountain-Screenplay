from rest_framework import viewsets

# Create your views here.

from .models import Frame
from .serializers import FrameSerializer


class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer
