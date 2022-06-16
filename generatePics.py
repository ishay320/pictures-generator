from random import randint, random
import cv2
import numpy as np
import utils


def create_solar_panel(
        base_ratio: float = 2, solar_resolution: int = 300, background_color=0, solar_border: int = 6, solar_border_color=1,
        split_half: bool = True, split_half_distance: int = 4, inside_blocks: bool = True,
        inside_blocks_x: int = 10, inside_blocks_y: int = 20, inside_blocks_separate: int = 1, inside_blocks_color=1,
        inside_blocks_tiny: bool = True, inside_blocks_tiny_number: int = 7, inside_blocks_tiny_color=0.) -> list:
    """
    creates one solar panel by the param that provided:
    @param base_ratio - the ratio of width and hight
    @param solar_resolution - the resolution of the short leg
    @param background_color - background color of the solar
    @param solar_border - borders of the solar in pixels
    @param solar_border_color - the borders color
    @param split_half - do you want to split it in half?
    @param split_half_distance - the 'borders' in pixels
    @param inside_blocks - the solar blocks
    @param inside_blocks_x - how many in the x 
    @param inside_blocks_y - how many in the y
    @param inside_blocks_separate - the size in pixel of the borders of the blocks
    @param inside_blocks_color - the color of the borders
    @param inside_blocks_tiny - the blocks inside the little blocks
    @param inside_blocks_tiny_number - how many
    @param inside_blocks_tiny_color - the border color of them
    @return image of solar panel
    """
    # create the solar
    solar_actual_hight = solar_resolution * base_ratio
    solar_actual_width = solar_resolution

    solar_panel = np.zeros((solar_actual_hight,
                           solar_actual_width))
    solar_panel.fill(background_color)

    # do the tiny blocks inside the little blocks
    if inside_blocks_tiny:
        for x_lines in range(0, solar_actual_hight, int(solar_actual_hight/(inside_blocks_y * inside_blocks_tiny_number))):
            solar_panel[x_lines:x_lines + 1] = inside_blocks_tiny_color

        for y_lines in range(0, solar_actual_width, int(solar_actual_width/(inside_blocks_x * inside_blocks_tiny_number))):
            solar_panel[:, y_lines:y_lines + 1] = inside_blocks_tiny_color

    # do the little blocks
    if inside_blocks:
        for x_lines in range(0, solar_actual_hight, int(solar_actual_hight/inside_blocks_y)):
            solar_panel[x_lines:x_lines +
                        inside_blocks_separate] = inside_blocks_color

    for y_lines in range(0, solar_actual_width, int(solar_actual_width/inside_blocks_x)):
        solar_panel[:, y_lines:y_lines +
                    inside_blocks_separate] = inside_blocks_color

    # split
    if split_half:
        solar_panel[int((solar_actual_hight / 2) - (split_half_distance / 2)):
                    int((solar_actual_hight / 2) + (split_half_distance / 2))] = solar_border_color

    # add borders
    solar_panel = np.pad(solar_panel, pad_width=solar_border,
                         mode='constant', constant_values=solar_border_color)
    solar_actual_hight += (2 * solar_border)
    solar_actual_width += (2 * solar_border)

    return solar_panel


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
solar_setting = {
    "base_ratio": 2, "solar_resolution": 300, "background_color": 0, "solar_border": 6,
    "split_half": True, "split_half_distance": 4,
    "inside_blocks": True, "inside_blocks_x": 10, "inside_blocks_y": 20, "inside_blocks_separate": 1, "inside_blocks_color": 1,
    "inside_blocks_tiny": True, "inside_blocks_tiny_number": 7, "inside_blocks_tiny_color": 0.5
}
solar_panel = create_solar_panel(**solar_setting)

# array setting
array_times_width = randint(1, 15)
array_times_hight = randint(1, 3)
array_space_width = 0.1
array_space_hight = 0.2

# array setting in the frame
frame_array_space_width = 1
frame_array_space_hight = 2

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
