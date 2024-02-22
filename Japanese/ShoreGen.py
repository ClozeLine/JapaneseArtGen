import numpy as np


def generate_sandy_fill(width, height, polygon_points, amplitude):
    # Create an empty array to store noise values
    noise_values = np.random.rand(height, width)

    # Generate noise values for each pixel within the generated polygon's boundaries
    for y in range(height):
        for x in range(width):
            if is_inside_polygon(x, y, polygon_points):

                # Normalize the value to the range [0, 1]
                value = noise_values[y][x]
                noise_values[y][x] = value * amplitude
    return noise_values


def is_inside_polygon(x, y, polygon_points):
    n = len(polygon_points)
    inside = False
    p1x, p1y = polygon_points[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon_points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def main(canvas):

    # Define sizes (based on canvas size)
    width = 800
    height = 800

    # Define the points for the polygon (this took forever holy shit)
    points = [(24, 775), (24, 550), (65, 553), (180, 560),  # top
              (187, 562), (185, 568), (183, 569),  # first shore
              (157, 580), (155, 583),  # first bay
              (265, 595), (380, 615), (480, 640),  # to second shore (not straight line)
              (490, 645), (493, 647),  (495, 649), (496, 650), (495, 652), (493, 653), (490, 655),  # second shore
              (475, 663), (465, 670), (465, 672), (475, 675), (540, 673), (580, 677),  # second bay
              (600, 679), (620, 684), (625, 686), (627, 687), (640, 691), (675, 700),  # curves
              (725, 711), (740, 715), (760, 718),  # curves
              (775, 719), (775, 775)]

    # Generate a "sandy" fill within the polygon's boundaries
    amplitude = 5
    sandy_fill = generate_sandy_fill(width, height, points, amplitude)

    # Apply the sandy fill
    for y in range(height):
        for x in range(width):
            if is_inside_polygon(x, y, points):
                value = sandy_fill[y][x]
                gray_value = int(150 + value * 40)
                canvas.putpixel((x, y), (gray_value, gray_value, gray_value))
