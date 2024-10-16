import json
import random
import time
from datetime import datetime, timezone, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import utils.format_utils as format_utils

from config.builder import Builder
from config.config import config
from logs import logger
from presentation.observer import Observable
from api_client import MempoolAPI

DATA_SLICE_DAYS = 1
DATETIME_FORMAT = "%Y-%m-%dT%H:%M"


def get_dummy_data():
    logger.info('Generating dummy data')



def main():
    logger.info('Initialize')

    data_sink = Observable()
    builder = Builder(config)
    builder.bind(data_sink)

    last_update_time = 0
    last_cycle_time = 0

    try:
        while True:
            current_time = time.time()

            # Check if it's time to update data
            if current_time - last_update_time >= config.refresh_interval:
                try:
                    data = MempoolAPI.get_all_data()
                    logger.info("Mempool data:")
                    logger.info(json.dumps(data['hashrate_data'], indent=2))
                    
                    data_sink.update_observers(data)
                    last_update_time = current_time
                except Exception as e:
                    logger.error(f"Error fetching data: {str(e)}")

            # Check if it's time to cycle pages
            if current_time - last_cycle_time >= config.page_cycle_interval:
                data_sink.cycle_pages()
                last_cycle_time = current_time

            time.sleep(0.1)  # Short sleep to prevent CPU overuse
    except IOError as e:
        logger.error(str(e))
    except KeyboardInterrupt:
        logger.info('Exit')
        data_sink.close()
        exit()


if __name__ == "__main__":
    main()
