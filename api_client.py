import requests
from logs import logger
import json
from config.config import config

class MempoolAPI:
    BASE_URL = "https://mempool.space/api"

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
    def get_braiins_data():
        try:
            url = "https://pool.braiins.com/accounts/profile/json/btc/"
            headers = {"SlushPool-Auth-Token": "mXtd4vht9DurQlT2"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.info("Raw Braiins API response:")
            logger.info(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            logger.error(f"Error fetching Braiins data: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error fetching Braiins data: {str(e)}")
            return {}

    @staticmethod
    def get_all_data():
        return {
            'hashrate_data': MempoolAPI.get_hashrate_data(),
            'braiins_data': MempoolAPI.get_braiins_data()
        }
