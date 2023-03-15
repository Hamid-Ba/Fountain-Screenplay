import os
import cv2
import numpy as np
from uuid import uuid4
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
        the_path = "/".join(the_path[the_path.index("media"):-1])
        return "/" + the_path
    
    # Fix URL
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
            black_white_image = self.path_to_save(the_image) + "/" + new_image_name + file_extension
                

            current_site = Site.objects.get_current()
            
            image_name = current_site.domain + self.domain_path_to_save(the_image) + "/"\
                + new_image_name + file_extension
            
            cv2.imwrite(black_white_image, img_binary)

            np_img = np.array(img_binary)
            np_img[np_img > 0] = 1

            return {"binary": np_img, "bw_image": image_name}
        except:
            pass

procces = ImageProcess()