import cv2 as cv
import numpy as np

class BottlePhoto:

    def __init__(self, path: str) -> None:

        self.img = cv.imread(path)
        self.bottle_brand: str = None
        self.liquid_in_bottle: bool = False
        self.shape_img: np.ndarray = None
        self.img_w_bounding_boxes: np.ndarray = None
        self.liquid_level: float = None
        self.img_with_bb_and_liquid_lvl: np.ndarray = None
        
        self.img_scaling()
    
    def img_scaling(self, scale: float = 0.25, img: str = "img") -> None:
        
        if img == "img":
            # setting up new width and height values by multiplying img width and height by scale
            width = int(self.img.shape[1] * scale)
            height = int(self.img.shape[0] * scale)
            size = (width, height)
            # changing img size to new values
            self.img = cv.resize(self.img, size, interpolation=cv.INTER_AREA)
        else:
            width = int(self.img_with_bb_and_liquid_lvl.shape[1] * scale)
            height = int(self.img_with_bb_and_liquid_lvl.shape[0] * scale)
            size = (width, height)
            self.img_with_bb_and_liquid_lvl = cv.resize(self.img_with_bb_and_liquid_lvl, size, interpolation=cv.INTER_AREA)