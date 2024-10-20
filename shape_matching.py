from bottle_photo import BottlePhoto
import cv2 as cv
import numpy as np

THRESHOLD_VALUE = 35
GAUS_BLUR_KERNEL = (13, 13)
MORPH_CLOSING_KERNEL = np.ones((7, 7), np.uint8)
PERCENT_LEFT_CROP = 3
BOTTLE_WIDTH_VAL = 160
WIT_SHAPE_EXAMPLE = "Photos/wit_bottle_shape.jpg"
RIVIVA_SHAPE_EXAMPLE = "Photos/riviva_bottle_shape.jpg"
SOMERSBY_SHAPE_EXAMPLE = "Photos/somersby_bottle_shape.jpg"

class ShapeMatching():

    def __init__(self, bottle: BottlePhoto) -> None:

        # attributes
        self.bottle = bottle
        self.problem_occurred = False
        self.raw_shape: np.ndarray = None
        self.cropped_img: np.ndarray = None
        self.cropped_adjusted: np.ndarray = None
        self.starting_bottle_width: int = None

        # executing methods
        self.get_bottle_shape()
        self.crop_shape()
        self.adjust_bottle_width()
        self.match_shape()

    
    def get_bottle_shape(self) -> None:
        """Method extracts bottle shape and creates new image with black background and white bottle shape."""
        
        # creating array with image in grayscale
        img_gray: np.ndarray = cv.cvtColor(self.bottle.img, cv.COLOR_BGR2GRAY)

        # adding blur to img_gray 
        img_gray = cv.GaussianBlur(img_gray, GAUS_BLUR_KERNEL, cv.BORDER_DEFAULT)

        # thresholding img with experimentally determined threshold value
        _, thresh = cv.threshold(img_gray, THRESHOLD_VALUE, 255, cv.THRESH_BINARY)

        # finding contours on thresholded image
        cnt, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

        # creating blank matrix that will be used to draw bottle shape - filled contour
        blank = np.zeros((img_gray.shape), dtype=np.uint8)
        
        # determining which one of found contours should be filled - last one is whole photo contour, second from the end is bottle contour
        x = len(cnt) - 1

        if (x < 0):
            # if this condition is met it means photo doesn't met requirements
            self.problem_occurred = True
        else:
            # filling contour
            shape = cv.fillPoly(blank, [cnt[x]], (255, 255, 255))
            # adding morphological transformation - closing
            shape = cv.morphologyEx(shape, cv.MORPH_CLOSE, MORPH_CLOSING_KERNEL)
            # attributes assignment
            self.raw_shape = shape
            self.bottle.shape_img = shape

    def crop_shape(self) -> None:
        """Method crops the raw bottle shape photo so there is a certain number of pixels left from shape to edge of image. 
        This pixels number is determined by PERCENT_LEFT_CROP global variable and amount of pixels in bottle shape widest point."""

        # getting lateral histogram to determine the object's location
        lat_hist_x = np.sum(self.raw_shape, 0)
        lat_hist_y = np.sum(self.raw_shape, 1)

        # getting object's coordinates from lateral histogram
        first_occ_x = np.argmax(lat_hist_x >= 2550)
        last_occ_x = len(lat_hist_x) - np.argmax(lat_hist_x[::-1] >= 2550) - 1
        first_occ_y = np.argmax(lat_hist_y >= 2550)
        last_occ_y = len(lat_hist_y) - np.argmax(lat_hist_y[::-1] >= 2550) - 1

        # calculating shape's width and height
        bottle_width = last_occ_x - first_occ_x
        bottle_height = last_occ_y - first_occ_y

        # calculating additional value
        if bottle_height > bottle_width:
            additional_val = int(bottle_height * PERCENT_LEFT_CROP / 100)
        else:
            additional_val = int(bottle_width * PERCENT_LEFT_CROP / 100)
        
        # calculating coordinates of rectangle that will be cropped from raw shape image
        x_r = last_occ_x + additional_val
        x_l = first_occ_x - additional_val
        y_b = last_occ_y + additional_val
        y_t = first_occ_y - additional_val

        # protection in case this values would be negative or higher than shape value
        if y_b > self.raw_shape.shape[0]:
            y_b =  self.raw_shape.shape[0]
        if y_t < 0:
            y_t = 0
        if x_r > self.raw_shape.shape[1]:
            x_r = self.raw_shape.shape[1]
        if x_l < 0:
            x_l = 0

        # updating attributes - cropping new image from raw shape img
        self.cropped_img = self.raw_shape[y_t:y_b,x_l:x_r]
        self.starting_bottle_width = bottle_width

    def adjust_bottle_width(self):
        """Method adjust image size to point where bottles width is equal global variable BOTTLE_WIDTH_VAL."""

        # calculating scale
        scale = BOTTLE_WIDTH_VAL / self.starting_bottle_width
        # calculating new height and new width values
        new_width = int(self.cropped_img.shape[1] * scale)
        new_height = int(self.cropped_img.shape[0] * scale)
        new_size = (new_width, new_height)
        # resizing and adding morphology closing operation
        new_img = cv.resize(self.cropped_img, new_size, interpolation = cv.INTER_AREA)
        self.cropped_adjusted = cv.morphologyEx(new_img, cv.MORPH_CLOSE, MORPH_CLOSING_KERNEL)      

    def match_shape(self) -> None:
        """Method determines bottle brand by matching its shape with shape examples of bottles of different brands and assigns brand name as attribute to BottlePhoto object."""

        # loading grayscale shape example images
        examples = [cv.cvtColor(cv.imread(WIT_SHAPE_EXAMPLE), cv.COLOR_BGR2GRAY), cv.cvtColor(cv.imread(RIVIVA_SHAPE_EXAMPLE), cv.COLOR_BGR2GRAY), cv.cvtColor(cv.imread(SOMERSBY_SHAPE_EXAMPLE), cv.COLOR_BGR2GRAY)]
        diff = []

        # using matchShapes function to match bottle shape with examples
        # the one example with lowest diff value is closes to shape of bottle, so you can assume this is brand of input bottle 
        for example in examples:
            diff.append(cv.matchShapes(self.cropped_adjusted, example, 1, 0.0))
        
        # finding lowest value and its index
        min_diff = min(diff)
        min_index = diff.index(min_diff)

        # assigning brand name to attribute of input BottlePhoto object
        if min_index == 0:
            self.bottle.bottle_brand = "DrWit"
        elif min_index == 1:
            self.bottle.bottle_brand = "Riviva"
        else:
            self.bottle.bottle_brand = "Somersby"