from random import randint, random
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

# solar setting
solar_width = 1
solar_hight = 2  # + (random() - 0.5)  # TODO: make it selectable

split = True
split_distance = 4

inside_blocks_x = 10
inside_blocks_y = 20
inside_blocks_separate = 1
inside_blocks_color = 1

inside_blocks_tiny = True
inside_blocks_tiny_number = 7
inside_blocks_tiny_color = 0.5


solar_resolution = 300
solar_border = 6

# array setting
array_times_width = randint(1, 15)
array_times_hight = randint(1, 3)
array_space_width = 0.1
array_space_hight = 0.2

# array setting in the frame
frame_array_space_width = 1
frame_array_space_hight = 2

# create the solar
solar_actual_hight = solar_resolution * solar_hight
solar_actual_width = solar_resolution * solar_width

solar_panel = np.zeros((solar_actual_hight,
                        solar_actual_width))

# do the tiny blocks
if inside_blocks_tiny:
    for x_lines in range(0, solar_actual_hight, int(solar_actual_hight/(inside_blocks_y * inside_blocks_tiny_number))):
        solar_panel[x_lines:x_lines + 1] = inside_blocks_tiny_color

    for y_lines in range(0, solar_actual_width, int(solar_actual_width/(inside_blocks_x * inside_blocks_tiny_number))):
        solar_panel[:, y_lines:y_lines + 1] = inside_blocks_tiny_color

# do the little blocks
for x_lines in range(0, solar_actual_hight, int(solar_actual_hight/inside_blocks_y)):
    solar_panel[x_lines:x_lines + inside_blocks_separate] = inside_blocks_color

for y_lines in range(0, solar_actual_width, int(solar_actual_width/inside_blocks_x)):
    solar_panel[:, y_lines:y_lines +
                inside_blocks_separate] = inside_blocks_color

# split
if split:
    solar_panel[int((solar_actual_hight / 2) - (split_distance / 2)):
                int((solar_actual_hight / 2) + (split_distance / 2))] = 1

# add borders
solar_panel = np.pad(solar_panel, pad_width=solar_border,
                     mode='constant', constant_values=1)
solar_actual_hight += (2 * solar_border)
solar_actual_width += (2 * solar_border)

print(solar_panel.shape)
cv2.imshow("solar", solar_panel)
cv2.waitKey(0)
# create the array


# paste it on the frame


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
