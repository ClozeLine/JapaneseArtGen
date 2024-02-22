import math

from PIL import Image, ImageDraw
import random
import torch

from ShoreGen import main

# Canvas
canvas_width = 800
canvas_height = 800
canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
draw = ImageDraw.Draw(canvas)

# top_of_ocean (global var)
top_of_ocean = int(canvas_height * 0.3)


def draw_sun():

    # Sun color and size
    sun_color = (random.randint(220, 255), 100, 70)  # Redness of sun
    size = random.randint(350, 450)

    # Generate bbox coordinates
    x0 = random.randint(25, 700)
    while x0 + size > 775:
        x0 = random.randint(100, 700)
    y0 = torch.distributions.Normal(top_of_ocean, 2)
    y0 = int(y0.sample()) // 2

    sun_center = (x0 + size // 2, y0 + size // 2)
    draw_rays(sun_center, size // 2)

    # Draw sun
    draw.ellipse((x0, y0, x0 + size, y0 + size), fill=sun_color)


def draw_ocean():
    # Color 1 fades to color 2
    end_color = (255, 255, 255)
    start_color = (25, 25, 25)

    # Coordinates for ocean generation
    x0, y0 = 25, top_of_ocean
    x1, y1 = canvas_width - 25, canvas_height - 25

    for y_ in range(y0, y1):
        # Interpolate color between start_color and end_color based on y position
        r = int(start_color[0] * (1 - (y_ - y0) / (y1 - y0)) + end_color[0] * ((y_ - y0) / (y1 - y0)))
        g = int(start_color[1] * (1 - (y_ - y0) / (y1 - y0)) + end_color[1] * ((y_ - y0) / (y1 - y0)))
        b = int(start_color[2] * (1 - (y_ - y0) / (y1 - y0)) + end_color[2] * ((y_ - y0) / (y1 - y0)))
        color = (r, g, b)
        draw.line([(x0, y_), (x1, y_)], fill=color)


def draw_sand(canv):
    # See ShoreGen.py
    main(canv)


def draw_boats():
    num_boats = random.randint(2, 8)

    # Variables for normal distribution
    distance_in_fleet_x_scale = 70
    distance_in_fleet_y_scale = 15

    # Generate in fleets if there are more than 4 boats
    fleets = True if num_boats > 4 else False

    # If there are fleets, divide into two fleets and make a center point for each
    if fleets:
        fleet_1_center_point = (random.randint(75, 725), random.randint(top_of_ocean + 35, 500))
        fleet_2_center_point = (random.randint(75, 725), random.randint(top_of_ocean + 35, 500))

    for i, boat in enumerate(range(num_boats)):

        # Generate coordinates for boats in first fleet, second fleet, or no fleet
        if fleets and i < 4:
            x0 = torch.distributions.Normal(fleet_1_center_point[0], distance_in_fleet_x_scale)
            y0 = torch.distributions.Normal(fleet_1_center_point[1], distance_in_fleet_y_scale)
        elif fleets and i >= 4:
            x0 = torch.distributions.Normal(fleet_2_center_point[0], distance_in_fleet_x_scale)
            y0 = torch.distributions.Normal(fleet_2_center_point[1], distance_in_fleet_y_scale)
        else:
            x0 = (random.randint(75, 725))
            y0 = (random.randint(top_of_ocean + 35, 500))

        # If coordinated were generated via normal distribution, sample a point from it
        if not isinstance(x0, int):
            x0 = int(x0.sample())
            y0 = int(y0.sample())

        # Length of the top of the sail
        top_x_len = random.randint(8, 12)

        # Length of the bottom of the sail (subtract on either side of bottom of sail)
        bottom_x_len_subtract = random.choice([1, 2])

        # Height of the sail
        y_len = random.randint(17, 22)

        # Sail coordinates
        tl = (x0, y0)
        tr = (x0 + top_x_len, y0)
        br = (x0 + top_x_len - bottom_x_len_subtract, y0 + y_len)
        bl = (x0 + bottom_x_len_subtract, y0 + y_len)

        # Generate mast
        line_up_top = ((x0 + top_x_len // 2), y0 - random.choice([1, 2, 3]))
        line_up_bottom = (line_up_top[0], line_up_top[1] + 7)

        # Generate boat body
        line_down_bottom = ((x0 + top_x_len // 2), y0 + y_len + random.choice([2, 3]))
        line_down_top = ((x0 + top_x_len // 2), br[1] - 7)

        # Draw all three boat components
        draw.line([(line_up_top[0], line_up_top[1]), (line_up_bottom[0]), line_up_bottom[1]],
                  fill='black', width=random.choice([2, 3]))
        draw.line([(line_down_top[0], line_down_top[1]), (line_down_bottom[0]), line_down_bottom[1]],
                  fill='black', width=(4 if bl[0] + br[0] > 2 else 2))
        draw.polygon([tl, tr, br, bl], fill='white', outline='black')


def draw_birds():
    num_birds = random.randint(4, 8)

    # Center point for normal distribution of birds
    bird_center_point = (random.randint(100, 700), random.randint(75, top_of_ocean - 35))

    for bird in range(num_birds):
        # Coordinates to place bird based on normal distribution around center point
        bird_center_point_x_dist = torch.distributions.Normal(bird_center_point[0], 40)
        bird_center_point_x = int(bird_center_point_x_dist.sample())
        bird_center_point_y_dist = torch.distributions.Normal(bird_center_point[1], 15)
        bird_center_point_y = int(bird_center_point_y_dist.sample())
        start_x = bird_center_point_x
        start_y = bird_center_point_y

        # Vary bird size
        wing_len = random.randint(18, 20)

        # Make bbox (one per wing)
        bbox1 = [(start_x, start_y), (start_x + wing_len, start_y + 20)]
        bbox2 = [(start_x + wing_len * 0.5, start_y), (start_x + wing_len * 0.5 + wing_len, start_y + 20)]
        start_angle = -120
        end_angle = -60

        # Draw each wing
        draw.arc(bbox1, start=start_angle, end=end_angle, fill="black", width=2)
        draw.arc(bbox2, start=start_angle, end=end_angle, fill="black", width=2)


def draw_borders():
    # Draw white borders
    draw.rectangle((0, 0, 25, 800), fill="white")
    draw.rectangle((775, 0, 800, 800), fill="white")
    draw.rectangle((25, 0, 775, 25), fill="white")
    draw.rectangle((25, 775, 775, 800), fill="white")


def draw_cloud():

    # Clouds on the right
    rect_info = ()
    cloud_num = random.randint(3, 6)
    start_y = torch.distributions.Normal(75, 50)
    start_y = int(start_y.sample())
    start_x = torch.distributions.Normal(600, 10)
    start_x = int(start_x.sample())
    for i in range(cloud_num):

        x_offset = random.randint(-50, 75)
        y_len = torch.distributions.Normal(20, 5)
        y_len = math.fabs(int(y_len.sample()))

        if i != 0:

            current_cloud_x_start = start_x + x_offset

            draw.rounded_rectangle(((current_cloud_x_start, rect_info[1]), (current_cloud_x_start + 300, rect_info[1] + y_len)),
                                   90, fill="white", outline='black')

            # If previous cloud starts before the current cloud, trace line from top of current
            if start_x + x_offset >= rect_info[0]:
                draw.line([(current_cloud_x_start + 10, rect_info[1]), (800, rect_info[1])], fill='white')

            # If previous cloud starts after the current cloud, trace line from bottom of previous
            else:
                draw.line([(rect_info[0] + 10, rect_info[1]), (800, rect_info[1])], fill='white')

            rect_info = (current_cloud_x_start,  rect_info[1] + y_len)
        else:
            draw.rounded_rectangle(((start_x + x_offset, start_y), (start_x + x_offset + 300, start_y + y_len)),
                                   90, fill="white", outline='black')

            rect_info = (start_x + x_offset, start_y + y_len)

    # Clouds on the left
    rect_info = ()
    cloud_num = random.randint(3, 6)
    start_y = torch.distributions.Normal(75, 50)
    start_y = int(start_y.sample())
    end_x = torch.distributions.Normal(200, 10)
    end_x = int(end_x.sample())
    for i in range(cloud_num):

        x_offset = random.randint(-50, 75)
        y_len = torch.distributions.Normal(20, 5)
        y_len = math.fabs(int(y_len.sample()))

        if i != 0:

            current_cloud_x_end = end_x + x_offset

            draw.rounded_rectangle(((-100, rect_info[1]), (current_cloud_x_end, rect_info[1] + y_len)),
                                   90, fill="white", outline='black')

            # If previous cloud starts before the current cloud, trace line from top of current
            if end_x + x_offset >= rect_info[0]:
                draw.line([(-100, rect_info[1]), (rect_info[0] - 10, rect_info[1])], fill='white')

            # If previous cloud starts after the current cloud, trace line from bottom of previous
            else:
                draw.line([(-100, rect_info[1]), (end_x + x_offset - 10, rect_info[1])], fill='white')

            rect_info = (current_cloud_x_end,  rect_info[1] + y_len)
        else:
            draw.rounded_rectangle(((-100, start_y), (end_x + x_offset, start_y + y_len)),
                                   90, fill="white", outline='black')

            rect_info = (end_x + x_offset, start_y + y_len)


def draw_rays(sun_center, radius):

    x0, y0 = sun_center

    for i, angle_degrees in enumerate(range(20, 360, 25)):
        angle_radians = math.radians(angle_degrees)

        # Calculate the coordinates of the endpoints of the line
        x1 = x0 + radius * math.cos(angle_radians)
        y1 = y0 + radius * math.sin(angle_radians)
        x2 = x0 + (radius + 800) * math.cos(angle_radians)
        y2 = y0 + (radius + 800) * math.sin(angle_radians)

        # Draw the line
        draw.line([(x1, y1), (x2, y2)], fill='black')

        # Calculate the coordinates of the endpoints of the triangle
        triangle_angle = math.radians(angle_degrees - 90)

        # Distance from the line (center) tips at base of triangle (ray)
        triangle_offset = 20

        x_triangle_left_side = x2 - triangle_offset * math.cos(triangle_angle)
        y_triangle_left_side = y2 - triangle_offset * math.sin(triangle_angle)
        x_triangle_right_side = x2 + triangle_offset * math.cos(triangle_angle)
        y_triangle_right_side = y2 + triangle_offset * math.sin(triangle_angle)

        # Draw the triangle
        draw.polygon([(x0, y0), (x_triangle_left_side, y_triangle_left_side),
                      (x_triangle_right_side, y_triangle_right_side)], fill=(120, 120, 120))


def draw_kakejiku():
    num_kakejiku = random.randint(0, 3)
    artwork_number_list = []
    kakejiku_list = []

    for i in range(num_kakejiku):

        artwork_number = random.randint(1, 3)
        while artwork_number in artwork_number_list:
            artwork_number = random.randint(1, 3)
        artwork_number_list.append(artwork_number)

        kanji = Image.open(f"Kakejiku/kakejiku_{artwork_number}.png")
        kanji.load()

        scaling_factor = 0.5

        kanji.thumbnail((int(kanji.width * scaling_factor), int(kanji.height * scaling_factor)))

        if i == 0:
            l_r = "right" if random.choice([0, 1]) == 0 else "left"
            t_b = "top" if random.choice([0, 1]) == 0 else "bottom"
        elif i == 1:
            l_r, t_b = kakejiku_list[0][1], kakejiku_list[0][2]
        elif i == 2:
            l_r = "right" if kakejiku_list[0][1] == "left" else "left"
            t_b = "top" if kakejiku_list[0][2] == "bottom" else "bottom"

        if l_r == "right":
            x0 = 785 - kanji.width
            y0 = 15
        else:
            x0 = 15
            y0 = 15

        if t_b == "bottom":
            y0 = y0 + 770 - kanji.height

        for kakejiku in kakejiku_list:
            if l_r == kakejiku[1] and t_b == kakejiku[2]:
                if l_r == "right" and t_b == "top":
                    x0 -= kakejiku[0].width
                    y0 += 15
                elif l_r == "left" and t_b == "top":
                    x0 += kakejiku[0].width
                    y0 += 15
                elif l_r == "left" and t_b == "bottom":
                    x0 += kakejiku[0].width
                    y0 -= 15
                elif l_r == "right" and t_b == "bottom":
                    x0 -= kakejiku[0].width
                    y0 -= 15

        kakejiku_list.append((kanji, l_r, t_b))

        canvas.paste(kanji, (x0, y0))


draw_sun()
draw_ocean()
draw_sand(canvas)
draw_boats()
draw_birds()
draw_cloud()
draw_borders()
draw_kakejiku()

# Add noise to final render
noise_factor = 0.1
noise = Image.new("L", (canvas_width, canvas_height))
for x in range(canvas_width):
    for y in range(canvas_height):
        noise.putpixel((x, y), random.randint(0, 255))
canvas = Image.blend(canvas, noise.convert('RGB'), noise_factor)

canvas.show()
