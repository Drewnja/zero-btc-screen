import requests
from logs import logger
import json
from config.config import config
from datetime import datetime, timezone, timedelta

class MempoolAPI:
    BASE_URL = "https://mempool.space/api"
    COINDESK_URL = "https://production.api.coindesk.com/v2/price/values"
    DATA_SLICE_DAYS = 1
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M"

    @staticmethod
    def get_fees():
        try:
            response = requests.get(f"{MempoolAPI.BASE_URL}/v1/fees/recommended")
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching fees: {str(e)}")
            return {}

    @staticmethod
    def get_hashrate_data():
        try:
            hashrate_period = config.hashrate_period
            response = requests.get(f"{MempoolAPI.BASE_URL}/v1/mining/hashrate/{hashrate_period}")
            response.raise_for_status()
            data = response.json()
            logger.info(f"Fetching hashrate data for period: {hashrate_period}")
            logger.info("Raw API response:")
            logger.info(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            logger.error(f"Error fetching hashrate data: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error fetching hashrate data: {str(e)}")
            return {}

    @staticmethod
    def get_mempool_data():
        return {
            'hashrate_data': MempoolAPI.get_hashrate_data()
        }

    @staticmethod
    def get_prices():
        logger.info('Fetching prices')
        timeslot_end = datetime.now(timezone.utc)
        end_date = timeslot_end.strftime(MempoolAPI.DATETIME_FORMAT)
        start_date = (timeslot_end - timedelta(days=MempoolAPI.DATA_SLICE_DAYS)).strftime(MempoolAPI.DATETIME_FORMAT)
        url = f'{MempoolAPI.COINDESK_URL}/{config.currency}?ohlc=true&start_date={start_date}&end_date={end_date}'
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            external_data = response.json()
            prices = [entry[1:] for entry in external_data['data']['entries']]
            return prices
        except requests.RequestException as e:
            logger.error(f"Error fetching prices: {str(e)}")
            return []

    @staticmethod
    def get_braiins_data():
        logger.info('Fetching Braiins data')
        url = 'https://pool.braiins.com/accounts/profile/json/btc/'
        headers = {"SlushPool-Auth-Token": "mXtd4vht9DurQlT2"}  # Consider moving this to a config file
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.info("Raw Braiins API response:")
            logger.info(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            logger.error(f"Error fetching Braiins data: {str(e)}")
            return {}

    @staticmethod
    def get_all_data():
        return {
            'hashrate_data': MempoolAPI.get_hashrate_data(),
            'prices': MempoolAPI.get_prices(),
            'braiins_data': MempoolAPI.get_braiins_data(),
        }
