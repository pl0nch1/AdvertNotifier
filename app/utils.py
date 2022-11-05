import logging
import random
import time

import numpy as np
import bezier
# import pyautogui

from selenium.webdriver.common.keys import Keys

LOGGER = logging.getLogger('general')
LOGGER.setLevel(logging.ERROR)


# def resting_mouse(): #move mouse to right of screen
#
#     start = pyautogui.position()
#     end = random.randint(1600,1750), random.randint(400,850)
#
#     x2 = (start[0] + end[0])/2 #midpoint x
#     y2 = (start[1] + end[1]) / 2 ##midpoint y
#
#     control1X = (start[0] + x2)/2
#     control2X = (end[0] + x2) / 2
#
#     # Two intermediate control points that may be adjusted to modify the curve.
#     control1 = control1X, y2 ##combine midpoints to create perfect curve
#     control2 = control2X, y2 ## using y2 for both to get a more linear curve
#
#     # Format points to use with bezier
#     control_points = np.array([start, control1, control2, end])
#     points = np.array([control_points[:, 0], control_points[:, 1]])  # Split x and y coordinates
#     # You can set the degree of the curve here, should be less than # of control points
#     degree = 3
#     # Create the bezier curve
#     curve = bezier.Curve(points, degree)
#
#     curve_steps = 50  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
#     delay = 0.003  # Time between movements. 1/curve_steps = 1 second for entire curve
#
#     # Move the mouse
#     for j in range(1, curve_steps + 1):
#         # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
#         # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
#         x, y = curve.evaluate(j / curve_steps)
#         pyautogui.moveTo(x, y)  # Move to point in curve
#         pyautogui.sleep(delay)  # Wait delay
#     time.sleep(.7 + random.random() % 0.6)


def write_text(element, text: str, accept=False):
    for c in text:
        element.send_keys(c)
        time.sleep(.01 + random.random() % 0.2)
    if accept:
        element.send_keys(Keys.ENTER)
