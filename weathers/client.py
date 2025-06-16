import requests
from urllib.parse import urljoin
import os
import logging
import traceback



class OpenMeteoClient:


    def __init__(self):
        self.__base_url = 'https://api.open-meteo.com/v1/'
        self.__default_params = {
            # 'latitude': os.environ['HAC_LATITUDE'],
            # 'longitude': os.environ['HAC_LONGITUDE'],
            # 'longitude': os.environ['HAC_TIMEZONE'],
            'latitude': 35.659,
            'longitude': 139.779,
            'timezone': 'Asia/Tokyo',
        }

    @property
    def default_params(self):
        return self.__default_params.copy()


    def forecast(self, **kwargs):
        params = {**self.default_params, **kwargs}
        return self.__get('forecast', params=params)
    

    def __get(self, endpoint, params=None):
        url = urljoin(self.__base_url, endpoint)
        try:
            res = requests.get(url, params=params)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            logging.error(f'Exception occured in {traceback.format_exc()}: {e}')
            return None