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
import locale


import json
import logging
from PIL import Image,ImageDraw,ImageFont

from weather.weather import WeatherHelper


def main():
    # Basic configuration settings (user replaceable)
    # config.json is in the root folder
    configFile = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json'))
    config = json.load(configFile)


    isDisplayConected = config['isDisplayConected']  # set to true when debugging rendering without displaying to screen
    screenWidth       = config['screenWidth']  # Width of E-Ink display. Default is landscape. Need to rotate image to fit.
    screenHeight      = config['screenHeight']  # Height of E-Ink display. Default is landscape. Need to rotate image to fit.
    imageWidth        = config['imageWidth']  # Width of image to be generated for display.
    imageHeight       = config['imageHeight'] # Height of image to be generated for display.
    rotateAngle       = config['rotateAngle']  # If image is rendered in portrait orientation, angle to rotate to fit screen
    hourFormat        = config['hourFormat'] # The format the hour will be displayed. eg. 13:02 or 01:02 PM
    latitude          = config['latitude'] # A float. The latitude for the Weather API.
    longitude         = config['longitude'] # A float. The longitude for the Weather API.
    timezone          = config['timezone'] # The timezone is necesary for the Weather API
    locales            = config['locales'] # Set the locales for the month name

    weatherService = WeatherHelper(latitude, longitude, timezone)
    weather_data = weatherService.fetch_open_meteo_data()

    locale.setlocale(locale.LC_TIME, locales)
    
    # Set the hour, this is important to see what time the e-Paper has been syncronized
    if hourFormat == "12h":
        time = dt.datetime.now().strftime("%I:%M %p")   
    else:
        time = dt.datetime.now().strftime("%H:%M")

    day = dt.datetime.now().strftime("%A, %d %b")


    assets = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets')
    weather_icons = os.path.join(assets, 'weather-icons')
    fonts = os.path.join(assets, 'fonts')
    # Drawing on the image
    font8 = ImageFont.truetype(os.path.join(os.path.join(fonts, 'pixel_operator'), 'PixelOperator8.ttf'), 8)
    font16 = ImageFont.truetype(os.path.join(os.path.join(fonts, 'pixel_operator'), 'PixelOperator.ttf'), 16)
    font16_bold = ImageFont.truetype(os.path.join(os.path.join(fonts, 'pixel_operator'), 'PixelOperator-Bold.ttf'), 16)



    image = Image.new('1', (imageWidth, imageHeight), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), f"{day}. {time}", font = font16_bold, fill = 0) # draw the current time in the top left corner

    # Frames
    draw.line([(0,16),(250,16)], fill = 0,width = 2) # Draw a line below the date
    draw.line([(90,17),(90,122)], fill = 0,width = 2) # Line dividing the screeen in two parts


    # Calendar icon
    cal_coordinates_x = 207
    cal_coordinates_y = 2

    cal_icon = Image.open(os.path.join(assets, "cal-icon3.bmp")) # calendar icon
    # This seems complicates, but it just draw a white rectangle bellow the calendar
    draw.rectangle([(cal_coordinates_x-2, cal_coordinates_y),(cal_coordinates_x + 28, cal_coordinates_y + 30)], fill = 255)
    image.paste(cal_icon, (cal_coordinates_x, cal_coordinates_y))

    # LEFT SEGMENT (WEATHER)
    # Todays information
    today_icon = weatherService.iconize_weather(weather_data["current_weather_code"])
    today_icon = Image.open(os.path.join(weather_icons, today_icon))
    image.paste(today_icon, (29,20))

    today_temperature = f"{str(weather_data['current_temperature_2m'])}°"
    draw.text((66,28), today_temperature, font = font16_bold, fill = 0) # The tomorrows temperature is bellow the icon


    #draw.text((160, 26), 'Agenda', font = font16_bold, fill = 0)

    # All the tomorrows information
    tomorrow_icon = weatherService.iconize_weather(weather_data["tomorrow_weather_code"])
    tomorrow_icon = Image.open(os.path.join(weather_icons, tomorrow_icon))
    image.paste(tomorrow_icon, (6,74)) # The icon is in the bottom left corner

    tomorrow_temperature = f"{str(weather_data['tomorrow_temperature_2m_max'])}/{str(weather_data['tomorrow_temperature_2m_min'])}°"
    draw.text((6,106), tomorrow_temperature, font = font16_bold, fill = 0) # The tomorrows temperature is bellow the icon

    # All the day after tomorrows information
    day_after_icon = weatherService.iconize_weather(weather_data["day_after_weather_code"])
    day_after_icon = Image.open(os.path.join(weather_icons, day_after_icon))
    image.paste(day_after_icon, (52,74))

    day_after_temperature = f"{str(weather_data['day_after_temperature_2m_max'])}/{str(weather_data['day_after_temperature_2m_min'])}°"
    draw.text((52,106), day_after_temperature, font = font16_bold, fill = 0)

    # RIGHT SEGMENT (CALENDAR/AGENDA)
    # TODO: writing this part and also the logic part

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
