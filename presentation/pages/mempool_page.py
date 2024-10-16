from .base_page import Page
from utils.format_utils import format_hash_rate, format_difficulty
from data.plot import Plot
from datetime import datetime
import logging

class MempoolPage(Page):
    def __init__(self, fonts):
        self.mempool_data = {}
        self.fonts = fonts
        logging.info("MempoolPage initialized")

    def render(self, draw, width, height):
        logging.info("MempoolPage render method called")
        logging.info(f"Mempool data keys: {self.mempool_data.keys()}")
        
        hashrate_data = self.mempool_data
        
        # Top part: Current Difficulty and Hashrate
        if 'currentDifficulty' in hashrate_data:
            diff = hashrate_data['currentDifficulty']
            formatted_diff = format_difficulty(diff)
            logging.info(f"Drawing difficulty: {formatted_diff}")
            draw.text((10, 5), "DIFF", font=self.fonts['small'], fill=0)
            draw.text((10, 20), formatted_diff, font=self.fonts['large'], fill=0)
            draw.text((10, 50), "T", font=self.fonts['medium'], fill=0)

        if 'currentHashrate' in hashrate_data:
            hashrate = hashrate_data['currentHashrate']
            formatted_hashrate = format_hash_rate(hashrate)
            logging.info(f"Drawing hashrate: {formatted_hashrate}")
            draw.text((width // 2, 5), "HASHRATE", font=self.fonts['small'], fill=0)
            draw.text((width // 2, 20), formatted_hashrate, font=self.fonts['large'], fill=0)
            draw.text((width // 2, 50), "EH/S", font=self.fonts['medium'], fill=0)

        # Bottom part: Hashrate and Difficulty graph
        if 'hashrates' in hashrate_data and 'difficulty' in hashrate_data:
            hashrate_values = [hr['avgHashrate'] / 1e18 for hr in hashrate_data['hashrates']]  # Convert to EH/s
            difficulty_values = [d['difficulty'] / 1e12 for d in hashrate_data['difficulty']]  # Convert to T
            timestamps = [hr['timestamp'] for hr in hashrate_data['hashrates']]
            
            if hashrate_values and difficulty_values:
                # Find the min and max for hashrate
                min_hashrate = min(hashrate_values)
                max_hashrate = max(hashrate_values)
                
                # Calculate positions for graph and labels
                graph_start_x = 30
                graph_width = width - graph_start_x - 10
                graph_height = height // 2 - 40
                graph_start_y = height // 2 + 20

                # Display max and min values for hashrate
                max_label = f"{max_hashrate:.0f}"
                min_label = f"{min_hashrate:.0f}"
                draw.text((5, graph_start_y), max_label, font=self.fonts['small'], fill=0)
                draw.text((5, graph_start_y + graph_height - 10), min_label, font=self.fonts['small'], fill=0)
                
                # Normalize hashrate
                norm_hashrate = [(h - min_hashrate) / (max_hashrate - min_hashrate) for h in hashrate_values]
                
                # Exaggerate difficulty changes
                diff_mean = sum(difficulty_values) / len(difficulty_values)
                diff_deviation = max(abs(d - diff_mean) for d in difficulty_values)
                amplification_factor = 5  # Adjust this value to increase/decrease exaggeration
                norm_difficulty = [0.5 + ((d - diff_mean) / diff_deviation) * 0.5 * amplification_factor for d in difficulty_values]
                
                # Clip normalized difficulty values to [0, 1] range
                norm_difficulty = [max(0, min(1, d)) for d in norm_difficulty]
                
                # Extend difficulty values to match hashrate length
                if len(norm_difficulty) < len(norm_hashrate):
                    norm_difficulty.extend([norm_difficulty[-1]] * (len(norm_hashrate) - len(norm_difficulty)))
                
                # Draw the graphs
                Plot.dual_line(norm_difficulty, norm_hashrate, size=(graph_width, graph_height), position=(graph_start_x, graph_start_y), draw=draw)

                # Add dates under the graph
                start_date = datetime.fromtimestamp(timestamps[0])
                end_date = datetime.fromtimestamp(timestamps[-1])
                draw.text((graph_start_x, height - 15), start_date.strftime("%d/%m"), font=self.fonts['small'], fill=0)
                draw.text((width - 40, height - 15), end_date.strftime("%d/%m"), font=self.fonts['small'], fill=0)

    def update_data(self, data, latest_price):
        self.mempool_data = data.get('hashrate_data', {})
        self.latest_price = latest_price
        logging.info(f"Updated MempoolPage data: {self.mempool_data}")
        logging.info(f"Latest price: {self.latest_price}")
