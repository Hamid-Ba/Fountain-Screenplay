import os
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from . import models
from tools.ImageProcessing import ImageProcess

process = ImageProcess()


@receiver(post_save, sender=models.Frame, dispatch_uid="frame_created")
def create_analyzed_image(sender, instance, created, **kwargs):
    if created:
        try:
            res = process.convert_to_binary(instance.orginal_image)
            bw_image = res["bw_image"]
            instance.analyze_frame(bw_image)

            res = process.do_all(instance.analyzed_image)
            instance.analyze_code(res["bits"], res["reverse_bits"])
            # bin_arr = res["binary"]
            # r_bin_arr = res["reverse_binary"]
            # analyzed_file_name = process.save_numpy_file(bin_arr)
            # r_analyzed_file_name = process.save_numpy_file(r_bin_arr)
            # instance.analyze_code(analyzed_file_name, r_analyzed_file_name)
        except:
            pass


@receiver(pre_delete, sender=models.Frame)
def delete_frame_with_all_belongs(sender, instance, *args, **kwargs):
    instance.orginal_image.delete()

    try:
        analyzed_image = instance.analyzed_image.split("/")[-1]
        image_path = "media/uploads/images"
        os.remove(f"{image_path}/{analyzed_image}")
        os.remove(f"{settings.BINARY_PATH}/{instance.binary_code}")
        os.remove(f"{settings.BINARY_PATH}/{instance.reverse_binary_code}")

    except:
        pass
