# serializers.py

from rest_framework import serializers

from .models import Frame


class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = "__all__"
        read_only_fields = ["code","analyzed_image"]