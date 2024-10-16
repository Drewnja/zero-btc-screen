from .base_page import Page
from data.plot import Plot

class PricePage(Page):
    def __init__(self, mode, fonts):
        self.prices = []
        self.mode = mode
        self.fonts = fonts

    def render(self, draw, width, height):
        if self.mode == "candle":
            Plot.candle(self.prices, size=(width - 45, 93), position=(41, 0), draw=draw)
        else:
            last_prices = [x[3] for x in self.prices]
            Plot.line(last_prices, size=(width - 42, 93), position=(42, 0), draw=draw)

        flatten_prices = [item for sublist in self.prices for item in sublist]
        Plot.y_axis_labels(flatten_prices, self.fonts['small'], (0, 0), (38, 89), draw=draw)
        draw.line([(10, 98), (width - 10, 98)])
        draw.line([(39, 4), (39, 94)])
        draw.line([(60, 102), (60, 119)])
        Plot.caption(flatten_prices[-1], 95, width, self.fonts['large'], draw)

        if len(self.prices) >= 2:
            x_middle = width // 1.8
            y_position = 5
            Plot.percentage(self.prices, x_middle, y_position, self.fonts['medium'], draw, fill=0)

    def update_data(self, data):
        self.prices = data['prices']

