#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
This project is designed for the WaveShare 12.48" eInk display. Modifications will be needed for other displays,
especially the display drivers and how the image is being rendered on the display. Also, this is the first project that
I posted on GitHub so please go easy on me. There are still many parts of the code (especially with timezone
conversions) that are not tested comprehensively, since my calendar/events are largely based on the timezone I'm in.
There will also be work needed to adjust the calendar rendering for different screen sizes, such as modifying of the
CSS stylesheets in the "render" folder.
"""
import datetime as dt
import sys


from display.display import DisplayHelper
import json
import logging
from PIL import Image,ImageDraw,ImageFont
import time


def main():
    # Basic configuration settings (user replaceable)
    configFile = open('config.json')
    config = json.load(configFile)

    displayTZ = config['displayTZ'] # list of timezones - print(pytz.all_timezones)
    isDisplayConected = config['isDisplayConected']  # set to true when debugging rendering without displaying to screen
    screenWidth = config['screenWidth']  # Width of E-Ink display. Default is landscape. Need to rotate image to fit.
    screenHeight = config['screenHeight']  # Height of E-Ink display. Default is landscape. Need to rotate image to fit.
    imageWidth = config['imageWidth']  # Width of image to be generated for display.
    imageHeight = config['imageHeight'] # Height of image to be generated for display.
    rotateAngle = config['rotateAngle']  # If image is rendered in portrait orientation, angle to rotate to fit screen


    if isDisplayConected:
        from display.display import DisplayHelper

        displayService = DisplayHelper(screenWidth, screenHeight)
        
        image = Image.open('assets/test.bmp')
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0,0),(50,50)],outline = 0)
        draw.rectangle([(55,0),(100,50)],fill = 0)
        draw.line([(0,0),(50,50)], fill = 0,width = 1)
        draw.line([(0,50),(50,0)], fill = 0,width = 1)
        draw.chord((10, 60, 50, 100), 0, 360, fill = 0)
        draw.ellipse((55, 60, 95, 100), outline = 0)
        draw.pieslice((55, 60, 95, 100), 90, 180, outline = 0)
        draw.pieslice((55, 60, 95, 100), 270, 360, fill = 0)
        draw.polygon([(110,0),(110,50),(150,25)],outline = 0)
        draw.polygon([(190,0),(190,50),(150,25)],fill = 0)


        displayService.update(image)  # go to sleep
        displayService.clear()
        displayService.sleep()  # go to sleep


if __name__ == "__main__":
    main()