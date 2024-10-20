# Bottle Inspection System

The project was created to allow the user to inspect the bottle by analyzing the photo. The program works only for specific bottles filled with liquid of a specific color and placed on a specific background. The photos used in the project were taken by me.

Used libraries: OpenCV, NumPy, PyQt5

## Program main stages:

1. Checking the bottle's brand.
2. Checking if there is a label on the bottle and adding bounding boxes around the label and cap (if they are present).
3. Checking if there is liquid inside the bottle and adding a line highlighting its level.

Each main stage of the program consists of smaller steps. The steps for each stage are listed below.

### Checking for the bottle's brand:

1. Getting an image of the bottle's shape.
2. Cropping the image and scaling it to set the bottle's width to a fixed value.
3. Comparing with example shapes.

### Checking if there is a label on the bottle and adding bounding boxes around the label and cap (if they are present):

1. Finding key points on the bottle photo and images with label examples.
2. Comparing the found key points and determining if there is a label that fits (or fits the most).
3. Checking the label and cap placement on the photo.
4. Adding bounding boxes to the photo.

### Checking if there is liquid inside the bottle and adding a line highlighting its level:

1. Changing the photo from BGR to HSV and adding masks.
2. Checking if there is liquid by checking for the number of pixels representing one of two possible colors of the fluid and comparing this number to the number of pixels that represent the bottle shape.
3. Checking the liquid level by using a lateral histogram and an image with pixels representing the liquid color colored white on a black background.
4. Adding a red line highlighting the liquid level to the photo.

# Demo:
## GUI:
![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/57697f7d-41ad-49e1-9a90-f460779e2539)

## View with original bottle photo:
![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/9d35fee3-a167-4d3d-b11f-027420042326)

## Veiw with processed photo:
![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/78b5ce1e-5d42-448b-bee6-0c87fb179c57)

## Different bottle inspection examples:
![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/cdee85a8-7489-45c8-bded-36d202c84185)

![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/cb483ede-ed5b-41f3-8317-5022409166dd)

![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/03f8b754-52df-46ef-9e5b-f747ea005133)

![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/554f325e-a4c5-4d33-8df7-c38ee23014d2)

![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/5052caf9-1480-4ce3-93e3-c8652b0b3845)
