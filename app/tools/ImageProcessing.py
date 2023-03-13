import os, cv2
import numpy as np
from uuid import uuid4

def image_file_path(instance, filename):
    """Generate file path for category image"""
    _, ext = os.path.splitext(filename)
    return os.path.join("uploads", "images", f"{instance.code}.{ext}")

class ImageProcess:

    def path_to_save(self,the_image):
        the_path = the_image.path
        the_path = the_path.split("/")[:-1]
        the_path = "/".join(the_path)
        return the_path
    
    def convert_to_binary(self,the_image):
        """Convert Image To Binary."""
        try:
            img_grey = cv2.imread(the_image.path, cv2.IMREAD_GRAYSCALE)
            
            # define a threshold, 128 is the middle of black and white in grey scale
            thresh = 128

            # threshold the image
            img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]

            #save image
            _ , file_extension = os.path.splitext(the_image.path)
            black_white_image = self.path_to_save(the_image) + "/" + str(uuid4()) + file_extension
            
            cv2.imwrite(black_white_image, img_binary) 

            np_img = np.array(img_binary)
            np_img[np_img > 0] = 1

            return {
                "binary" : np_img,
                "bw_image" : black_white_image
            }
        except :
            pass