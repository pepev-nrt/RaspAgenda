#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
This script is created to test the different fonts installed. It may return error if some of them are missing.
"""
import datetime as dt
import json
import os
import sys

from PIL import Image,ImageDraw,ImageFont


def main():
    # Basic configuration settings (user replaceable)
    # config.json is in the root folder
    configFile = open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'config.json'))
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


    assets = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'assets')
    fontsdir = os.path.join(assets, 'fonts')
    # Drawing on the image
    font15 = ImageFont.truetype(os.path.join(fontsdir, 'wavesharefont.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(fontsdir, 'wavesharefont.ttc'), 24)

    # pixel_operator fonts
    font8 = ImageFont.truetype(os.path.join(os.path.join(fontsdir, 'pixel_operator'), 'PixelOperator8.ttf'), 8)
    font8_bold = ImageFont.truetype(os.path.join(os.path.join(fontsdir, 'pixel_operator'), 'PixelOperator8-Bold.ttf'), 8)
    font16 = ImageFont.truetype(os.path.join(os.path.join(fontsdir, 'pixel_operator'), 'PixelOperator.ttf'), 16)
    font16_bold = ImageFont.truetype(os.path.join(os.path.join(fontsdir, 'pixel_operator'), 'PixelOperator-Bold.ttf'), 16)

    # Better VCR font
    font16_2 = ImageFont.truetype(os.path.join(fontsdir, 'Better VCR 9.0.1.ttf'), 16)
    font8_2 = ImageFont.truetype(os.path.join(fontsdir, 'Better VCR 9.0.1.ttf'), 12)


    image = Image.new('1', (imageWidth, imageHeight), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)


    draw.text((0, 0), f"Pixel Operator 16 bold", font = font16_bold, fill = 0)
    draw.text((0, 16), f"Hacer la compra", font = font16, fill = 0)
    draw.text((0, 32), f"Pasear al gato", font = font16, fill = 0)
    draw.text((0, 48), f"Escribir un post en Mastodon", font = font16, fill = 0)



    image.save(os.path.join(assets, 'test-characters.bmp'))


    if isDisplayConected:
        # This line is necesary to be able to acceass the modules from this folder
        # We are basically adding the root folder of the proyect to the path
        sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        from display.display import DisplayHelper

        displayService = DisplayHelper(screenWidth, screenHeight)
        displayService.update(image.rotate(rotateAngle))
        displayService.clear()
        displayService.sleep()  # go to sleep


if __name__ == "__main__":
    main()
