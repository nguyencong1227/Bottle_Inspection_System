from bottle_photo import BottlePhoto
import cv2 as cv
import numpy as np

# global variables that stores photos paths
# caps are only for Rivia and DrWit bottles and are single photo because it looks the same in every photo
WIT_LABEL_TEMPLATES = ["Label_Templates/wit1.png", "Label_Templates/wit2.png", "Label_Templates/wit3.png", "Label_Templates/wit4.png", "Label_Templates/wit5.png", "Label_Templates/wit6.png", "Label_Templates/wit7.png", "Label_Templates/wit8.png", "Label_Templates/wit9.png"]
WIT_CAP_TEMPLATE = "Label_Templates/wit_cap.png"
RIVIVA_LABEL_TEMPLATE = ["Label_Templates/riviva_label.png"]
RIVIVA_CAP_TEMPLATE = "Label_Templates/riviva_cap.png"
SOMERSBY_LABEL_TEMPLATES = ["Label_Templates/somer1.png", "Label_Templates/somer2.png", "Label_Templates/somer3.png"]

# global variables defining program work / bounding box appearance
GOOD_MATCHES_MIN_NUMBER = 12
BOUNDING_BOX_COLOR = (0, 255, 255)
BOUNDING_BOX_LINE_THICKNESS = 4

class LabelDetection:

    def __init__(self, bottle: BottlePhoto) -> None:
        
        self.bottle = bottle
        self.label_img: np.ndarray = None
        self.cap_img: np.ndarray = None
        self.no_label_fits: bool = None
        self.img_w_bounding_boxes: np.ndarray = None

        self.detect_label()
        self.draw_bounding_boxes()

    def label_comparison(self, template: np.ndarray) -> int:
        """Method returns number of key points that are accepted as good match."""

        # finding key points in label example and bottle photo
        orb = cv.ORB_create()
        kp_img, des_img = orb.detectAndCompute(self.bottle.img, None)
        kp_label, des_label = orb.detectAndCompute(template, None)
        bf = cv.BFMatcher()

        # finding matching key points
        matches = bf.knnMatch(des_img, des_label, k = 2)

        # determining how many of found key points are good match
        good_matches_count = 0
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches_count += 1
        
        # returning number of good matches
        return good_matches_count

    def detect_label(self):
        """Method determines if there is label on bottle, and if there is one it also determines which one of examples is most similar, then assigns its image as attribute label_img."""

        # defining best_match_val value and templates list
        best_match_val = 0
        templates: list [np.ndarray] = []

        # creating list of images that are used for comparison for bottle's brand 
        if self.bottle.bottle_brand == "DrWit":
            for single_template in WIT_LABEL_TEMPLATES:
                new_img = cv.imread(single_template)
                new_img = cv.resize(new_img, (int(0.25 * new_img.shape[1]), int(0.25 * new_img.shape[0])))
                templates.append(new_img)

        elif self.bottle.bottle_brand == "Riviva":
            for single_template in RIVIVA_LABEL_TEMPLATE:
                new_img = cv.imread(single_template)
                new_img = cv.resize(new_img, (int(0.25 * new_img.shape[1]), int(0.25 * new_img.shape[0])))
                templates.append(new_img)
        
        else:
            for single_template in SOMERSBY_LABEL_TEMPLATES:
                new_img = cv.imread(single_template)
                new_img = cv.resize(new_img, (int(0.25 * new_img.shape[1]), int(0.25 * new_img.shape[0])))
                templates.append(new_img)
        
        # comparing photo to label examples and finding best
        for index, template in enumerate(templates):
            good_matches_count = self.label_comparison(template = template)
            if good_matches_count > best_match_val:
                best_match_val = good_matches_count
                best_match_index = index

        # deciding if best found example is good enough to establish there is label based on good match points counted
        if best_match_val > GOOD_MATCHES_MIN_NUMBER:
            # assigning attribute values
            self.label_img = templates[best_match_index]
            self.no_label_fits = False
        
        else:
            # assigning attribute value
            self.no_label_fits = True

    def get_object_placement(self, object: str = "cap") -> int:
        """Method returns value of image height for top and bottom edge of cap or label placement in photo. """

        # defining cap example photo as object_img variable
        if object == "cap":
            # choosing right cap example image
            if self.bottle.bottle_brand == "DrWit":
                self.cap_img = cv.imread(WIT_CAP_TEMPLATE)
                self.cap_img = cv.resize(self.cap_img, (int(0.25 * self.cap_img.shape[1]), int(0.25 * self.cap_img.shape[0])))
                object_img = self.cap_img

            elif self.bottle.bottle_brand == "Riviva":
                self.cap_img = cv.imread(RIVIVA_CAP_TEMPLATE)
                self.cap_img = cv.resize(self.cap_img, (int(0.25 * self.cap_img.shape[1]), int(0.25 * self.cap_img.shape[0])))
                object_img = self.cap_img
        
        # defining label example image as object_img variable
        else:
            object_img = self.label_img

        # getting object height
        height, _, _ = object_img.shape
        
        # using openCV function to find coordinates in which object placement is most possible
        res = cv.matchTemplate(object_img, self.bottle.img, cv.TM_SQDIFF_NORMED)
        _, _, min_loc, _ = cv.minMaxLoc(res)

        # calculating coordinates
        top_left = min_loc
        top = top_left[1]
        bottom = top + height

        # returning top and bottom edge of object height
        return top, bottom

    def draw_single_bounding_box(self, object: str):
        """Method draws single bounding box around label or cap based on input object string."""

        # getting coordinates
        top, bottom = self.get_object_placement(object = object)

        # middle is used to calculate correct bounding box width
        middle = (bottom + top) // 2

        # getting right and left values based on bottle shape edges in middle height value
        left = next(i for i, val in enumerate(self.bottle.shape_img[middle]) if val > 0)
        right = self.bottle.shape_img.shape[1] - next(i for i, val in enumerate(reversed(self.bottle.shape_img[middle])) if val > 0)

        # drawing rectangle based on calculated coordinates
        self.img_w_bounding_boxes =  cv.rectangle(self.img_w_bounding_boxes, [left, top], [right, bottom], BOUNDING_BOX_COLOR, BOUNDING_BOX_LINE_THICKNESS)

    def draw_bounding_boxes(self):
        """Method draws bounding boxes around cap and label(if they are in the picture)."""

        # copying img because it will be edited
        self.img_w_bounding_boxes = self.bottle.img.copy()

        if self.bottle.bottle_brand != "Somersby":
            self.draw_single_bounding_box("cap")

        if self.no_label_fits is False:
            self.draw_single_bounding_box("label")
        
        self.bottle.img_w_bounding_boxes = self.img_w_bounding_boxes