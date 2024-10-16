import os
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
try:
    from waveshare_epd import epd2in13_V2
except ImportError:
    pass
from presentation.observer import Observer
from presentation.page_manager import PageManager
from config.config import config
from logs import logger
from api_client import MempoolAPI

SCREEN_HEIGHT = 122
SCREEN_WIDTH = 250

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Roses.ttf'), 8)

FONT_MEDIUM = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 16)

FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 26)

class Epd2in13v2(Observer):

    def __init__(self, observable, mode, rotation=0):
        super().__init__(observable=observable)
        self.epd = self._init_display()
        self.mode = mode
        self.rotation = int(rotation)  # Ensure rotation is an integer
        
        fonts = {
            'small': FONT_SMALL,
            'medium': FONT_MEDIUM,
            'large': FONT_LARGE
        }
        
        self.page_manager = PageManager(mode, fonts)
        self.current_data = None
        logger.info(f"Full refresh will occur every {config.full_refresh_page_count} page changes")

    @staticmethod
    def _init_display():
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)
        epd.init(epd.PART_UPDATE)
        return epd

    def form_image(self):
        image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        draw = ImageDraw.Draw(image)
        current_page = self.page_manager.get_current_page()
        current_page.render(draw, SCREEN_WIDTH, SCREEN_HEIGHT)
        return image.rotate(self.rotation)

    def update(self, data):
        self.current_data = MempoolAPI.get_all_data()
        self.page_manager.update_data(self.current_data)
        self._render()

    def _check_and_cycle_page(self):
        need_full_refresh = self.page_manager.cycle_page()
        logger.info(f"Cycling to page: {type(self.page_manager.get_current_page()).__name__}")
        if self.current_data:
            if need_full_refresh:
                self.full_refresh()
            else:
                self._render()

    def _render(self):
        image = self.form_image()
        buffer = self.epd.getbuffer(image)
        self.epd.displayPartial(buffer)

    def full_refresh(self):
        logger.info("Performing full refresh for Epd2in13v2")
        self.epd.init(self.epd.FULL_UPDATE)
        image = self.form_image()
        buffer = self.epd.getbuffer(image)
        self.epd.display(buffer)
        self.epd.init(self.epd.PART_UPDATE)

    def close(self):
        self.epd.sleep()
