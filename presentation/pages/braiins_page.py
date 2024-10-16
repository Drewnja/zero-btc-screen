from .base_page import Page
import logging

class BraiinsPage(Page):
    def __init__(self, fonts):
        self.fonts = fonts
        self.braiins_data = {}
        logging.info("BraiinsPage initialized")

    def render(self, draw, width, height):
        logging.info("BraiinsPage render method called")
        
        if not self.braiins_data:
            draw.text((10, height // 2), "No Braiins data available", font=self.fonts['medium'], fill=0)
            return

        btc_data = self.braiins_data.get('btc', {})
        
        # Display username
        draw.text((10, 5), f"User: {self.braiins_data.get('username', 'N/A')}", font=self.fonts['small'], fill=0)
        
        # Display hashrates
        draw.text((10, 25), f"5m: {btc_data.get('hash_rate_5m', 'N/A')} {btc_data.get('hash_rate_unit', '')}", font=self.fonts['small'], fill=0)
        draw.text((10, 40), f"60m: {btc_data.get('hash_rate_60m', 'N/A')} {btc_data.get('hash_rate_unit', '')}", font=self.fonts['small'], fill=0)
        draw.text((10, 55), f"24h: {btc_data.get('hash_rate_24h', 'N/A')} {btc_data.get('hash_rate_unit', '')}", font=self.fonts['small'], fill=0)
        
        # Display worker status
        draw.text((10, 75), f"Workers: OK:{btc_data.get('ok_workers', 'N/A')} Low:{btc_data.get('low_workers', 'N/A')}", font=self.fonts['small'], fill=0)
        draw.text((10, 90), f"Off:{btc_data.get('off_workers', 'N/A')} Dis:{btc_data.get('dis_workers', 'N/A')}", font=self.fonts['small'], fill=0)
        
        # Display rewards
        draw.text((10, 110), f"Today: {btc_data.get('today_reward', 'N/A')} BTC", font=self.fonts['small'], fill=0)
        draw.text((10, 125), f"Est: {btc_data.get('estimated_reward', 'N/A')} BTC", font=self.fonts['small'], fill=0)
        draw.text((10, 140), f"Balance: {btc_data.get('current_balance', 'N/A')} BTC", font=self.fonts['small'], fill=0)

    def update_data(self, data):
        self.braiins_data = data.get('braiins_data', {})
        logging.info(f"Updated Braiins data: {self.braiins_data}")
