from .base_page import Page
import logging
from PIL import Image, ImageDraw, ImageFont
from decimal import Decimal

class BraiinsPage(Page):
    def __init__(self, fonts):
        self.fonts = fonts
        self.braiins_data = {}
        self.background = Image.open("assets/braiins_page.png")
        self.latest_price = 0.0
        logging.info(f"BraiinsPage initialized. Background image mode: {self.background.mode}")

    def render(self, draw, width, height):
        logging.info("BraiinsPage render method called")
        
        # Force the image into '1' mode and invert it
        image = self.background.copy().convert('1').point(lambda x: 255 - x)
        draw_on_image = ImageDraw.Draw(image)
        
        if not self.braiins_data:
            logging.warning("No Braiins data available")
            self.draw_centered_text(draw_on_image, "No Braiins data", (width // 2, height // 2), self.fonts['medium'], 255)
        else:
            btc_data = self.braiins_data.get('btc', {})
            logging.info(f"BTC data: {btc_data}")
            
            # Convert and draw 5min hashrate
            hashrate_5m = self.convert_to_ths(btc_data.get('hash_rate_5m', 0))
            self.draw_centered_text(draw_on_image, f"{hashrate_5m:.2f}", (185, 67), self.fonts['large'], 255)
            
            # Convert and draw 24h hashrate
            hashrate_24h = self.convert_to_ths(btc_data.get('hash_rate_24h', 0))
            self.draw_centered_text(draw_on_image, f"{hashrate_24h:.2f}", (185, 99), self.fonts['medium'], 255)

            # Draw worker information
            self.draw_centered_text(draw_on_image, str(btc_data.get('ok_workers', 0)), (160, 17), self.fonts['medium'], 255)
            self.draw_centered_text(draw_on_image, str(btc_data.get('low_workers', 0)), (226, 17), self.fonts['medium'], 255)
            self.draw_centered_text(draw_on_image, str(btc_data.get('off_workers', 0)), (160, 47), self.fonts['medium'], 255)
            self.draw_centered_text(draw_on_image, str(btc_data.get('dis_workers', 0)), (226, 47), self.fonts['medium'], 255)

            # Convert and draw today's reward in USD
            today_reward_btc = float(btc_data.get('today_reward', 0))
            logging.info(f"Today's reward in BTC: {today_reward_btc}")
            logging.info(f"Latest price: {self.latest_price}")
            today_reward_usd = today_reward_btc * self.latest_price
            logging.info(f"Calculated reward in USD: {today_reward_usd}")
            self.draw_centered_text(draw_on_image, f"${today_reward_usd:.2f}", (60, 50), self.fonts['large'], 255)

            # Convert and draw current balance in USD
            current_balance_btc = float(btc_data.get('current_balance', 0))
            logging.info(f"Current balance in BTC: {current_balance_btc}")
            current_balance_usd = current_balance_btc * self.latest_price
            logging.info(f"Calculated balance in USD: {current_balance_usd}")
            self.draw_centered_text(draw_on_image, f"${current_balance_usd:.2f}", (60, 100), self.fonts['large'], 255)

        logging.info("About to call draw.bitmap()")
        draw.bitmap((0, 0), image)
        logging.info("draw.bitmap() called")
        
        logging.info("Render complete")

    def update_data(self, data, latest_price):
        self.braiins_data = data.get('braiins_data', {})
        self.latest_price = latest_price
        logging.info(f"Updated Braiins data: {self.braiins_data}")
        logging.info(f"Updated latest price: {self.latest_price}")

    def convert_to_ths(self, hashrate):
        # Assuming the input is in Gh/s, convert to Th/s
        return hashrate / 1000

    def draw_centered_text(self, draw, text, position, font, fill):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = position[0] - text_width // 2
        y = position[1] - text_height // 2
        draw.text((x, y), text, font=font, fill=fill)
