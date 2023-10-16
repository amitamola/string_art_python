import matplotlib.pyplot as plt
%matplotlib inline

from PIL import Image, ImageDraw, ImageOps


import cv2
import numpy as np

def display_image(img):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.imshow(img, cmap='gray')


def crop_circle(image_path):
    # Open the input image as numpy array, convert to RGB
    img = Image.open(image_path).convert("RGB")
    npImage = np.array(img)
    h, w = img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    npAlpha = np.array(alpha)

    # Add alpha layer to RGB
    npImage = np.dstack((npImage, npAlpha))

    # Convert numpy array to PIL Image
    pilImage = Image.fromarray(npImage)

    # Crop the image to the circle
    pilImage = pilImage.crop((0, 0, h, w))
    pilImage = ImageOps.fit(pilImage, (2 * min(h, w),) * 2, Image.Resampling.LANCZOS)

    # Save the image
    pilImage.save('cropped_circle.png')
    return pilImage


img_out = crop_circle('my_img.jpg')


import math
from PIL import Image, ImageDraw

def create_canvas_with_points(n, point_radius=2):
    #List to save all the points
    points = []
    
    # Load the cropped circle image
    circle_img = Image.open('cropped_circle.png')

    # Get the size of the circle image
    width, height = circle_img.size

    # Create a new image with the same size as the circle image
    canvas_img = Image.new('RGB', (width, height), color='white')

    # Calculate the radius of the circle
    radius = width // 2

    # Calculate the angle between each point
    angle = 2 * math.pi / n

    # Calculate the distance between each point
    distance = radius - 10

    # Draw the points on the canvas
    draw = ImageDraw.Draw(canvas_img)
    for i in range(n):
        x = int(radius + distance * math.cos(i * angle))
        y = int(radius + distance * math.sin(i * angle))
        draw.ellipse((x-point_radius, y-point_radius, x+point_radius, y+point_radius), fill='black')
        points.append((x-point_radius, y-point_radius, x+point_radius, y+point_radius))

    # Save the canvas image
    canvas_img.save('canvas.png')

    return canvas_img, points

