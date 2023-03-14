from rest_framework import viewsets

# Create your views here.

from .models import Frame
from .serializers import FrameSerializer


class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.order_by("-id")
    serializer_class = FrameSerializer
