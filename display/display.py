#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
This part of the code exposes functions to interface with the eink display
"""

import display.epd2in13_V4 as eink
from PIL import Image
import logging


class DisplayHelper:

    def __init__(self, width, height):
        # Initialise the display
        self.logger = logging.getLogger('raspagenda')
        self.screenwidth = width
        self.screenheight = height
        self.epd = eink.EPD()
        self.epd.init()

    def update(self, img):
        # Updates the display with the grayscale and red images
        # start displaying on eink display
        # self.epd.clear()
        self.epd.display(self.epd.getbuffer(img))
        self.logger.info('E-Ink display update complete.')

    def calibrate(self, cycles=1):
        # Calibrates the display to prevent ghosting
        white = Image.new('1', (self.epd.screenwidth, self.screenheight), 255)
        black = Image.new('1', (self.screenwidth, self.screenheight), 0)
        for _ in range(cycles):
            self.epd.display(self.epd.getbuffer(black))
            self.epd.display(self.epd.getbuffer(white))
            self.epd.display(self.epd.getbuffer(black))
            self.epd.display(self.epd.getbuffer(white))
        self.logger.info('E-Ink display calibration complete.')

    def sleep(self):
        # send E-Ink display to deep sleep
        self.epd.sleep()
        self.logger.info('E-Ink display entered deep sleep.')

    def clear(self):
        # clear E-Ink display
        self.epd.Clear(0xFF)
        self.logger.info('E-Ink display entered deep sleep.')
