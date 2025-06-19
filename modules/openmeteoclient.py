import os
import logging
import traceback
from urllib.parse import urljoin
import requests



class OpenMeteoClient:


    WEATHERCODE_MSP = {
        0: '晴れ',
        1: '主に晴れ',
        2: '曇りがち',
        3: '曇り',
        45: '霧',
        48: '霧（霧氷）',
        51: '弱い霧雨',
        53: '中程度の霧雨',
        55: '強い霧雨',
        61: '弱い雨',
        63: '中程度の雨',
        65: '強い雨',
        71: '弱い雪',
        73: '中程度の雪',
        75: '強い雪',
        80: '弱いにわか雨',
        81: 'にわか雨',
        82: '激しいにわか雨',
    }

    ALL_DAILY_PARAMS = [
        'weathercode',
        'temperature_2m_min',
        'temperature_2m_max',
        'temperature_2m_mean',
        'apparent_temperature_min',
        'apparent_temperature_max',
        'apparent_temperature_mean',
        'sunshine_duration',
        'shortwave_radiation_sum',
        'uv_index_max',
        'et0_fao_evapotranspiration',
        'rain_sum',
        'precipitation_hours',
        'cloud_cover_min',
        'cloud_cover_max',
        'cloud_cover_mean',
        'windspeed_10m_max',
        'windgusts_10m_max',
    ]

    DEFAULT_DAILY_PARAMS = [
        'weathercode',
        'temperature_2m_max', # ℃
        'temperature_2m_min', # ℃
        'temperature_2m_mean', # ℃
        'relative_humidity_2m_mean', # %
        'windspeed_10m_max', # km/h
    ]

    DEFAULT_HOURLY_PARAMS = [
        'weathercode',
        'temperature_2m', # ℃
        'apparent_temperature', # ℃
        'relative_humidity_2m', # %
        'rain', # mm
        'precipitation_probability', # %
        'cloud_cover', # %
        'windspeed_10m', # km/h
        'shortwave_radiation', # W/m²
        'uv_index'
    ]

    def __init__(self, session=None):
        self.session = session or requests.Session()
        self.__base_url = 'https://api.open-meteo.com/v1/'
        self.__base_params = {
            # 'latitude': os.environ['HAC_LATITUDE'],
            # 'longitude': os.environ['HAC_LONGITUDE'],
            # 'timezone': os.environ['HAC_TIMEZONE'],
            'latitude': 35.659,
            'longitude': 139.779,
            'timezone': 'Asia/Tokyo',
        }

    @property
    def base_params(self):
        return self.__base_params.copy()


    def forecast(self, **kwargs):
        params = {**self.base_params, **kwargs}
        return self.__get('forecast', params=params)
    

    def archive(self, **kwargs):
        params = {**self.base_params, **kwargs}
        return self.__get('archive', params=params)
    

    def __get(self, endpoint, params=None):
        url = urljoin(self.__base_url, endpoint)
        try:
            res = self.session.get(url, params=params, timeout=10) 
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            logging.error(traceback.format_exc())
            return None