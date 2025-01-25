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

    print(config)

if __name__ == "__main__":
    main()