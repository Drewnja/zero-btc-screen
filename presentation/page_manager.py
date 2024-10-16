import time
import logging
from logs import logger
from config.config import config
from presentation.pages.price_page import PricePage
from presentation.pages.mempool_page import MempoolPage
from presentation.pages.braiins_page import BraiinsPage
from api_client import MempoolAPI

class PageManager:
    def __init__(self, mode, fonts):
        self.pages = [
            PricePage(mode, fonts),
            MempoolPage(fonts),
            BraiinsPage(fonts),
        ]
        self.current_page_index = 0
        self.page_change_count = 0
        self.full_refresh_page_count = config.full_refresh_page_count

    def get_current_page(self):
        return self.pages[self.current_page_index]

    def cycle_page(self):
        self.current_page_index = (self.current_page_index + 1) % len(self.pages)
        self.page_change_count += 1
        logger.info(f"Cycled to page index: {self.current_page_index}")
        return self.page_change_count % self.full_refresh_page_count == 0  # Return True if it's time for a full refresh

    def update_data(self, data):
        all_data = MempoolAPI.get_all_data()
        logging.info(f"All data keys: {all_data.keys()}")
        latest_price = all_data['latest_price']
        logging.info(f"Latest price from API: {latest_price}")
        for page in self.pages:
            page.update_data(all_data, latest_price)
