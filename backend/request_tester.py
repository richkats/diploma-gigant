# -*- coding: utf-8 -*-
import json
from pprint import pprint

import requests as req
from faker import Faker
from faker_music import MusicProvider


SERVER = "http://localhost:8000/"


def make_request(server, method, payload):
    if method == 'get':
        r = req.get(server)
    elif method == 'post':
        r = req.post(server, json=payload)
    elif method == 'delete':
        r = req.delete(server, json=payload)
    return r.text


def generate_fake_users(number):
    fake = Faker()
    fake_users = []
    for i in range(number):
        fake_user = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "nickname": fake.user_name(),
            "email": fake.free_email(),
            "photo": fake.image_url(),
            "password": fake.password(length=12)
        }
        fake_users.append(fake_user)
    return fake_users


def generate_random_genres(number):
    fake = Faker()
    fake.add_provider(MusicProvider)
    fake_genres = []
    for i in range(number):
        fake_genre = {
            "name": fake.music_subgenre()
        }
        fake_genres.append(fake_genre)
    return fake_genres


def provide_multiple_creation(server, func, number):
    for item in func(number):
        print(make_request(server, 'post', item))


if __name__ == "__main__":
    provide_multiple_creation(SERVER+"genres/", generate_random_genres, 8)