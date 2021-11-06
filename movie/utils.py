import os

import certifi
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']
KINOPOISK_API_KEY = os.environ['KINOPOISK_API_KEY']

ca = certifi.where()
client = MongoClient(MONGODB_URI, tlsCAFile=ca)

db = client['kekino']


def get_movie_frames(movie_id, api_key=KINOPOISK_API_KEY):
    url = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{movie_id}/frames'
    headers = {'X-API-KEY': KINOPOISK_API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()['frames']


