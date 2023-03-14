import os
from django.db import models
from uuid import uuid4

# Create your models here.


def image_file_path(instance, filename):
    """Generate file path for category image"""
    _, ext = os.path.splitext(filename)
    return os.path.join("uploads", "images", f"{instance.code}.{ext}")


def music_file_path(instance, filename):
    """Generate file path for category image"""
    _, ext = os.path.splitext(filename)
    return os.path.join("uploads", "music", f"{instance.code}.{ext}")


class FrameManager(models.Manager):
    """Frame Manager"""

    def fill_analyzed_image(self, frame_id, image):
        frame = self.filter(id=frame_id).first()
        frame.analyzed_image = image
        frame.save()


class Frame(models.Model):
    """Frame Model"""

    class FrameType(models.TextChoices):
        IMAGE = "I", "Image"
        TEXT = "T", "Text"

    code = models.UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    type = models.CharField(
        max_length=1, default=FrameType.IMAGE, choices=FrameType.choices
    )
    title = models.CharField(max_length=125, null=False, blank=False)
    orginal_image = models.ImageField(null=False, upload_to=image_file_path)
    analyzed_image = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
    )
    duration = models.DurationField(null=True, blank=True)
    x_axis = models.IntegerField(default=0)
    y_axis = models.IntegerField(default=0)

    objects = FrameManager()

    def __str__(self) -> str:
        return self.title

    def fill_analyzed_image(self, image):
        self.analyzed_image = image
        self.save()


class Package(models.Model):
    """Collection Frame Model"""

    order = models.IntegerField(null=False, blank=False)
    repeat = models.IntegerField(null=True, blank=True, default=1)

    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.frame.title + " " + self.order + " " + self.repeat


class Fountain(models.Model):
    """Collection Model"""

    code = models.UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    title = models.CharField(max_length=125, null=False, blank=False)
    packages = models.ManyToManyField(Package, related_name="fountains")
    music = models.FileField(null=True, blank=True, upload_to=music_file_path)

    def __str__(self) -> str:
        return self.title
