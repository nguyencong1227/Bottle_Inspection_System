from bottle_photo import BottlePhoto
from shape_matching import ShapeMatching
from detecting_label import LabelDetection
from liquid_level_detection import LiquidLevelDetection

def bottle_inspection_system(file_name: str, logger):

    # performing all operations on photo
    bottle = BottlePhoto(path=file_name)
    shape_matching = ShapeMatching(bottle)
    label_detection = LabelDetection(bottle)
    liquid_level_detection = LiquidLevelDetection(bottle)
    bottle.img_scaling(scale = 0.66, img = "img")
    bottle.img_scaling(scale = 0.66, img = "final")

    # communication to user
    logger(f"In the picture is a bottle of {bottle.bottle_brand}.")
    if label_detection.no_label_fits is False:
        logger("The bottle has a label.")
    if liquid_level_detection.liquid_presence is True:
        logger(f"There is liquid in the bottle. Liquid level is at {bottle.liquid_level}% of the bottle height.")
        if label_detection.no_label_fits is False:
            logger("Caution! Given liquid level value may be incorrect, because of possibility of liquid presence behind label.")
    else:
        logger("The bottle is empty.")

    # returning original image and processed image
    return bottle.img, bottle.img_with_bb_and_liquid_lvl

