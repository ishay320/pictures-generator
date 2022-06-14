import cv2
import numpy as np
import utils

# setting
seed: int = 69
width: int = 1920
hight: int = 1080
name_format = "{0}/{1}.jpg"
csv_file = open("database.csv", "w")
csv_file.write("file name,x0,y0,x1,y1,x2,y2,x3,y3\n")

# Frame creation
frame = np.ones((hight, width))
frame *= 255

# background creation
frame = np.random.rand(hight, width)*255

# solar creation
np.random.seed(seed)
points = []
for _ in range(4):
    y = np.random.randint(0, hight)
    x = np.random.randint(0, width)
    points.append((x, y))
print(points)
print(np.array([utils.order_points(np.array(points))]))
points_sorted = np.array([utils.order_points(np.array(points))])
frame = cv2.fillPoly(frame, points_sorted, (0, 0, 0))

# csv creation
image_number = 1
image_name = '{:06d}'.format(image_number)
csv_string = f'{name_format.format("genFrames",image_name)}'
for point in points_sorted[0]:
    for pos in point:
        csv_string += f",{pos}"
csv_file.write(csv_string)
csv_file.write("\n")

# image saving
cv2.imwrite(name_format.format("genFrames", image_name), frame)
