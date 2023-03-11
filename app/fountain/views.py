from rest_framework import mixins,generics,viewsets

# Create your views here.

from .models import Frame
from .serializers import FrameSerializer


class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer