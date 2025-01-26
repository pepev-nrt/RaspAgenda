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
import os
import sys


import json
import logging
from PIL import Image,ImageDraw,ImageFont


def main():
    # Basic configuration settings (user replaceable)
    # config.json is in the root folder
    configFile = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json'))
    config = json.load(configFile)


    isDisplayConected = config['isDisplayConected']  # set to true when debugging rendering without displaying to screen
    screenWidth = config['screenWidth']  # Width of E-Ink display. Default is landscape. Need to rotate image to fit.
    screenHeight = config['screenHeight']  # Height of E-Ink display. Default is landscape. Need to rotate image to fit.
    imageWidth = config['imageWidth']  # Width of image to be generated for display.
    imageHeight = config['imageHeight'] # Height of image to be generated for display.
    rotateAngle = config['rotateAngle']  # If image is rendered in portrait orientation, angle to rotate to fit screen
    hourFormat = config['hourFormat'] # The format the hour will be displayed. eg. 13:02 or 01:02 PM

    # Set the hour, this is important to see what time the e-Paper has been syncronized
    if hourFormat == "12h":
        time = dt.datetime.now().strftime("%I:%M %p")   
    else:
        time = dt.datetime.now().strftime("%H:%M")


    assets = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets')
    fonts = os.path.join(assets, 'fonts')
    # Drawing on the image
    font15 = ImageFont.truetype(os.path.join(fonts, 'wavesharefont.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(fonts, 'wavesharefont.ttc'), 24)
    font8 = ImageFont.truetype(os.path.join(os.path.join(fonts, 'pixel_operator'), 'PixelOperator8.ttf'), 8)
    font16 = ImageFont.truetype(os.path.join(os.path.join(fonts, 'pixel_operator'), 'PixelOperator.ttf'), 16)
    font16_bold = ImageFont.truetype(os.path.join(os.path.join(fonts, 'pixel_operator'), 'PixelOperator-Bold.ttf'), 16)



    #image = Image.open('assets/test4.bmp')
    image = Image.new('1', (imageWidth, imageHeight), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), time, font = font16_bold, fill = 0) # draw the current time in the top left corner

    draw.line([(0,16),(250,16)], fill = 0,width = 2)
    draw.line([(125,16),(125,122)], fill = 0,width = 2)

    cal_icon = Image.open(os.path.join(assets, "cal-icon3.bmp"))

    image.paste(cal_icon, (129,20))

    draw.text((160, 26), 'Agenda', font = font16_bold, fill = 0)

    # draw.line([(0,50),(50,0)], fill = 0,width = 1)
    # draw.chord((10, 60, 50, 100), 0, 360, fill = 0)
    # draw.ellipse((55, 60, 95, 100), outline = 0)
    # draw.pieslice((55, 60, 95, 100), 90, 180, outline = 0)
    # draw.pieslice((55, 60, 95, 100), 270, 360, fill = 0)
    # draw.polygon([(110,0),(110,50),(150,25)],outline = 0)
    # draw.polygon([(190,0),(190,50),(150,25)],fill = 0)
    # draw.rectangle([(0,0),(50,50)],outline = 0)

    image.save(os.path.join(assets, 'output.bmp'))



    if isDisplayConected:
        from display.display import DisplayHelper

        displayService = DisplayHelper(screenWidth, screenHeight)
        displayService.update(image.rotate(rotateAngle)) # Displays the image
        #displayService.clear()
        displayService.sleep()  # go to sleep


if __name__ == "__main__":
    main()
