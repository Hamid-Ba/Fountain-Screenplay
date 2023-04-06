import os
import cv2
import numpy as np
from uuid import uuid4
from django.conf import settings
from django.contrib.sites.models import Site


IMAGE_PATH = "media/uploads/images"


class ImageProcess:
    def path_to_save(self, the_image):
        the_path = the_image.path
        the_path = the_path.split("/")[:-1]
        the_path = "/".join(the_path)
        return the_path

    def domain_path_to_save(self, the_image):
        the_path = the_image.path
        the_path = the_path.split("/")
        the_path = "/".join(the_path[the_path.index("media") : -1])
        return "/" + the_path

    def convert_to_binary(self, the_image):
        """Convert Image To Binary."""
        try:
            img_grey = cv2.imread(the_image.path, cv2.IMREAD_GRAYSCALE)

            # define a threshold, 128 is the middle of black and white in grey scale
            thresh = 128

            # threshold the image
            img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]

            new_image_name = str(uuid4())
            # save image
            _, file_extension = os.path.splitext(the_image.path)
            black_white_image = (
                self.path_to_save(the_image) + "/" + new_image_name + file_extension
            )

            current_site = Site.objects.get_current()

            image_name = (
                current_site.domain
                + self.domain_path_to_save(the_image)
                + "/"
                + new_image_name
                + file_extension
            )

            cv2.imwrite(black_white_image, img_binary)

            np_img = np.array(img_binary)
            np_img[np_img > 0] = 1
            np_reverse = np.logical_not(np_img).astype(int)

            return {
                "binary": np_img,
                "reverse_binary": np_reverse,
                "bw_image": image_name,
            }
        except:
            pass

    def save_numpy_file(self, file):
        try:
            file_name = f"{str(uuid4())}.npy"

            if not os.path.exists(settings.BINARY_PATH):
                os.mkdir(settings.BINARY_PATH)

            with open(f"{settings.BINARY_PATH}/{file_name}", "wb") as f:
                np.save(f, file)

            return file_name
        except:
            return False

    def read_numpy_file(self, file_name):
        with open(f"media/binaryFile/{file_name}", "rb") as f:
            return np.load(f)

    def do_all(self, analyzed_image):
        """make binary matrix of analyzed image"""
        analyzed_image = analyzed_image.split("/")[-1]

        img = cv2.imread(
            f"{IMAGE_PATH}/{analyzed_image}", cv2.IMREAD_GRAYSCALE
        )  # The image pixels have range [0, 255]
        img //= 255  # Now the pixels have range [0, 1]
        img_list = img.tolist()  # We have a list of lists of pixels

        result = ""
        for row in img_list:
            row_str = [str(p) for p in row]
            result += "[" + ", ".join(row_str) + "],\n"

        bits = result
        reverse_bits = result.replace("1", "2").replace("0", "1").replace("2", "0")

        return {"bits": bits, "reverse_bits": reverse_bits}


procces = ImageProcess()
