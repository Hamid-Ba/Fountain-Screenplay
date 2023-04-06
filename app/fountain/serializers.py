# serializers.py

from rest_framework import serializers

from . import models


class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Frame
        fields = "__all__"
        read_only_fields = [
            "code",
            "analyzed_image",
            "binary_code",
            "reverse_binary_code",
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["binary_code"] = None
        rep["reverse_binary_code"] = None

        return rep


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package
        fields = "__all__"


class FountainSerializer(serializers.ModelSerializer):
    packages = PackageSerializer(many=True, required=False)

    class Meta:
        model = models.Fountain
        fields = "__all__"
        read_only_fields = ["code", "music"]

    def _create_packages(self, packages):
        packs_id = []
        for pack in packages:
            pack = models.Package.objects.create(
                order=pack["order"],
                repeat=pack["repeat"],
                frame=pack["frame"],
                is_reverse=pack["is_reverse"],
            )
            packs_id.append(pack.id)

        return packs_id

    def _relate_fount_to_packages(self, fount, packs_id):
        for pack in packs_id:
            pack = models.Package.objects.get(id=pack)
            fount.packages.add(pack)

    def validate(self, attrs):
        if attrs.get("packages") is None:
            msg = "enter packages please"
            raise serializers.ValidationError(msg)
        return attrs

    def create(self, validated_data):
        packs = validated_data.pop("packages", None)
        packs_id = self._create_packages(packs)

        fount = models.Fountain.objects.create(**validated_data)
        fount.save()
        self._relate_fount_to_packages(fount, packs_id)

        return fount

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["packages"] = []
        packs = instance.packages.all()
        for pack in packs:
            pack = models.Package.objects.get(id=pack.id)
            rep["packages"].append(
                {
                    "id": pack.id,
                    "order": pack.order,
                    "repeat": pack.repeat,
                    "reverse": pack.is_reverse,
                    "frame": {
                        "id": pack.frame.id,
                        "code": pack.frame.code,
                        "title": pack.frame.title,
                    },
                }
            )

        return rep


class FountainMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fountain
        fields = ["music"]
