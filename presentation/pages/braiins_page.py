from .base_page import Page

class BraiinsPage(Page):
    def __init__(self, fonts):
        self.fonts = fonts
        self.hashrate_5m = 0
        self.hashrate_unit = "Gh/s"

    def render(self, draw, width, height):
        # Display 5-minute hashrate
        hashrate_text = f"{self.hashrate_5m:.2f} {self.hashrate_unit}"
        text_width, text_height = draw.textsize(hashrate_text, font=self.fonts['large'])
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        draw.text((x, y), hashrate_text, font=self.fonts['large'], fill=0)

        # Display "5m Hashrate" label
        label = "5m Hashrate"
        label_width, label_height = draw.textsize(label, font=self.fonts['small'])
        label_x = (width - label_width) // 2
        label_y = y + text_height + 5
        draw.text((label_x, label_y), label, font=self.fonts['small'], fill=0)

    def update_data(self, data):
        if 'braiins_data' in data and 'btc' in data['braiins_data']:
            btc_data = data['braiins_data']['btc']
            self.hashrate_5m = btc_data.get('hash_rate_5m', 0)
            self.hashrate_unit = btc_data.get('hash_rate_unit', 'Gh/s')
