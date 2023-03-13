from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models
from tools.ImageProcessing import ImageProcess

procces = ImageProcess()

@receiver(post_save, sender=models.Frame, dispatch_uid="frame_created")
def create_analyzed_image(sender, instance, created, **kwargs):
    if created:
        try:
            bw_image = procces.convert_to_binary(instance.orginal_image)[
                "bw_image"
            ]
            instance.fill_analyzed_image(bw_image)
        except:
            pass