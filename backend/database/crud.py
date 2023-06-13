import asyncio
import random
import time
from datetime import datetime
from functools import cache

from geopy import Yandex, Nominatim, GeoNames

from . import db_manager as models, schemas, regions
from typing import List


# Users CRUD


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def create_user(user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db_user.save()
    return db_user


def delete_users(user_ids: List[int]):
    user_ids = list(user_ids)
    print(user_ids)
    q = models.User.delete().where(models.User.id << user_ids)
    print(q)
    return q.execute()


# Genre CRUD


def create_genre(genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.dict())
    db_genre.save()
    return db_genre


def get_genre(genre_id: int):
    return models.Genre.filter(models.Genre.id == genre_id).first()


def get_genre_by_name(name: str):
    return models.Genre.filter(models.Genre.name == name).first()


def get_genres(skip: int = 0, limit: int = 100):
    return list(models.Genre.select().offset(skip).limit(limit))


async def get_genre_names_from_list(genre_list: list):
    return [genre.name for genre in models.Genre.filter(models.Genre.id << genre_list)]


def delete_genres(genre_ids: List[int]):
    genre_ids = list(genre_ids)
    print(genre_ids)
    q = models.Genre.delete().where(models.Genre.id << genre_ids)
    print(q)
    return q.execute()


# Requirement CRUD


def create_requirement(requirement: schemas.RequirementCreate):
    db_requirement = models.Requirement(**requirement.dict())
    db_requirement.save()
    return db_requirement


def get_requirement(requirement_id: int):
    return models.Requirement.filter(models.Requirement.id == requirement_id).first()


def get_requirement_by_name(name: str):
    return models.Requirement.filter(models.Requirement.name == name).first()


def get_requirements(skip: int = 0, limit: int = 100):
    return list(models.Requirement.select().offset(skip).limit(limit))


async def get_requirements_from_list(req_list: list):
    return [{"name": requirement.name, "value": requirement.value} for requirement in
            models.Requirement.filter(models.Requirement.id << req_list)]


def delete_requirements(requirement_ids: List[int]):
    requirement_ids = list(requirement_ids)
    print(requirement_ids)
    q = models.Requirement.delete().where(models.Requirement.id << requirement_ids)
    print(q)
    return q.execute()


# Advertisement CRUD


def create_advertisement(ad: schemas.AdvertisementCreate):
    db_ad = models.Advertisement(**ad.dict())
    db_ad.save()
    return db_ad


def get_advertisement(ad_id: int):
    return models.Advertisement.filter(models.Advertisement.id == ad_id).first()


def get_advertisement_by_name(name: str):
    return models.Advertisement.filter(models.Advertisement.name == name).first()


def get_advertisements(skip: int = 0, limit: int = 100):
    return list(models.Advertisement.select().offset(skip).limit(limit))


def delete_advertisement(ad_ids: List[int]):
    ad_ids = list(ad_ids)
    print(ad_ids)
    q = models.Advertisement.delete().where(models.Advertisement.id << ad_ids)
    print(q)
    return q.execute()


# Artist CRUD


def create_artist(artist: schemas.ArtistCreate):
    db_artist = models.Artist(**artist.dict())
    db_artist.save()
    return db_artist


def get_artist(artist_id: int):
    return models.Artist.filter(models.Artist.id == artist_id).first()


def get_artist_by_name(name: str):
    return models.Artist.filter(models.Artist.name == name).first()


def get_artists(skip: int = 0, limit: int = 100):
    return list(models.Artist.select().offset(skip).limit(limit))


def delete_artists(artist_ids: List[int]):
    artist_ids = list(artist_ids)
    print(artist_ids)
    q = models.Artist.delete().where(models.Artist.id << artist_ids)
    print(q)
    return q.execute()


# Artist_Ad CRUD


def create_artist_ad(artist_ad: schemas.ArtistAdCreate):
    db_artist_ad = models.Artist_Ad(**artist_ad.dict())
    db_artist_ad.save()
    return db_artist_ad


def get_artist_ad(artist_ad_id: int):
    return models.Artist_Ad.filter(models.Artist_Ad.id == artist_ad_id).first()


def get_artist_ad_by_name(name: str):
    return models.Artist_Ad.filter(models.Artist_Ad.name == name).first()


def get_artist_ads(skip: int = 0, limit: int = 100):
    return list(models.Artist_Ad.select().offset(skip).limit(limit))


def delete_artist_ad(artist_ad_ids: List[int]):
    artist_ad_ids = list(artist_ad_ids)
    print(artist_ad_ids)
    q = models.Artist_Ad.delete().where(models.Artist_Ad.id << artist_ad_ids)
    print(q)
    return q.execute()


# def city_to_coords(city: str):
#     # locator = Yandex(api_key="8aeb294a-cc6e-4270-a6b3-8f7cbfe62021", user_agent="Gigant")
#     locator = GeoNames(username="g1gant", user_agent="Gigant")
#     location = locator.geocode(city)
#
#     if location is None:
#         return 61.2500000, 73.4166700
#     return location.latitude, location.longitude
#
#
# async def coords_to_city(latitude, longitude):
#     # locator = Yandex(api_key="641dc78b-a22e-4ceb-a28d-2717683f052e", user_agent=f"Gigant{random.randint(0, 99999)}")  # 8aeb294a-cc6e-4270-a6b3-8f7cbfe62021
#     # locator = Nominatim(user_agent=f"Gigant{random.randint(0, 99999)}")
#     locator = GeoNames(username="g1gant", user_agent="Gigant")
#     # location = locator.reverse(f"{latitude}, {longitude}")
#     location = locator.reverse(f"{latitude}, {longitude}", lang="ru")
#     city = location.address.split(",")[-2].strip()
#     #if city not in ["Санкт-Петербург", "Москва", "Севастополь", "Челябинск", "Самара"]:
#     if city in regions.regions:
#         city = location.address.split(",")[-3].strip()
#     return city


def artist_ad_processer(props):
    # print(props)
    artist = get_artist_by_name(props.name)
    if artist is None:
        artist_dict = {"name": props.name, "photos": [props.photo], "city": props.city,
                       "contacts": props.contacts, "start_date": int(datetime.now().timestamp()),
                       "owner": 847266099681296385}
        artist = create_artist(schemas.ArtistCreate.parse_obj(artist_dict))
    # solution 1 (easy)
    genre_list = []
    all_genres = get_genres()
    for genre in props.genres:
        if genre not in all_genres:
            genre = create_genre(schemas.GenreCreate.parse_obj({"name": genre}))
        else:
            genre = get_genre_by_name(genre)
        genre_list.append(genre.id)  # ?
    reqs = props.requirements
    req_list = [create_requirement(schemas.RequirementCreate.parse_obj(req)).id for req in reqs]
    # for req in reqs:
    #     r = create_requirement(schemas.RequirementCreate.parse_obj(req))
    #     req_list.append(r.id)
    artist_ad_dict = {"owner": 847266099681296385, "short_name": props.name, "text": props.description,
                      "requirements": req_list, "genres": genre_list, "date": props.free_dates[0], "status": "new",
                      "artist": artist.id, "city": props.city, "equipment": props.equipment}
    artist_ad = create_artist_ad(schemas.ArtistAdCreate.parse_obj(artist_ad_dict))
    return artist_ad


async def process_artist_ad(artist_ad):
    ad_id = artist_ad.id
    name = artist_ad.short_name
    requirements = await get_requirements_from_list(artist_ad.requirements)
    genres = await get_genre_names_from_list(
        artist_ad.genres[:3] if len(artist_ad.genres) >= 3 else artist_ad.genres[:3])
    dt = artist_ad.date
    photo = artist_ad.artist.photos[0]
    city = artist_ad.city
    artist_ad_dict = {
        "ad_id": ad_id,
        "type": "artist_ad",
        "name": name,
        "requirements": requirements,
        "genres": genres,
        "date": dt,
        "photo": photo,
        "city": city
    }
    return artist_ad_dict


async def get_all_artist_ads():
    artist_ads = get_artist_ads()
    ads = []
    tasks = [asyncio.create_task(process_artist_ad(artist_ad)) for artist_ad in artist_ads]
    ads = await asyncio.gather(*tasks)
    return ads


def get_all_artist_ads_temp():
    artist_ads = get_artist_ads()
    ads = []
    for artist_ad in artist_ads:
        ad_id = artist_ad.id
        name = artist_ad.short_name
        requirements = get_requirements_from_list(artist_ad.requirements)
        genres = get_genre_names_from_list(artist_ad.genres)
        dt = artist_ad.date
        photo = artist_ad.artist.photos[0]
        city = artist_ad.city
        artist_ad_dict = {"ad_id": ad_id, "name": name, "requirements": requirements,
                          "genres": genres, "date": dt, "photo": photo, "city": city}
        ads.append(artist_ad_dict)
    return ads


# def artist_ad_to_short_dict(artist_ad):
#     artist_ad_dict = {"ad_id": artist_ad.id, "name": artist_ad.short_name,
#                       "requirements": get_requirements_from_list(artist_ad.requirements),
#                       "genres": get_genre_names_from_list(artist_ad.genres), "date": artist_ad.date,
#                       "photo": artist_ad.artist.photos[0], "city": coords_to_city(artist_ad.lat, artist_ad.long)}
#     return artist_ad_dict
#
#
# def get_all_artist_ads_mapped():
#     t0 = time.time()
#     artist_ads = get_artist_ads()
#     ads = list(map(artist_ad_to_short_dict, artist_ads))
#     t1 = time.time()
#     print(t1-t0)
#     return ads


async def get_rendered_artist_ad(ad_id: int):
    artist_ad = get_artist_ad(ad_id)
    ad_id = artist_ad.id
    name = artist_ad.short_name
    requirements = await get_requirements_from_list(artist_ad.requirements)
    genres = await get_genre_names_from_list(artist_ad.genres)
    dt = artist_ad.date
    photo = artist_ad.artist.photos[0]
    description = artist_ad.text
    status = artist_ad.status
    equipment = artist_ad.equipment
    contacts = artist_ad.artist.contacts
    city = artist_ad.city
    artist_ad_dict = {"ad_id": ad_id, "name": name, "requirements": requirements,
                      "genres": genres, "date": dt, "photo": photo, "description": description,
                      "equipment": equipment, "status": status, "contacts": contacts, "city": city, "type": "artist_ad"}
    return artist_ad_dict


# Venue CRUD


def create_venue(venue: schemas.VenueCreate):
    db_venue = models.Venue(**venue.dict())
    db_venue.save()
    return db_venue


def get_venue(venue_id: int):
    return models.Venue.filter(models.Venue.id == venue_id).first()


def get_venue_by_name(name: str):
    return models.Venue.filter(models.Venue.name == name).first()


def get_venues(skip: int = 0, limit: int = 100):
    return list(models.Venue.select().offset(skip).limit(limit))


def delete_venues(venue_ids: List[int]):
    venue_ids = list(venue_ids)
    # print(artist_ids)
    q = models.Venue.delete().where(models.Venue.id << venue_ids)
    # print(q)
    return q.execute()


# Venue Ad CRUD


def create_venue_ad(venue_ad: schemas.VenueAdCreate):
    db_venue_ad = models.Venue_Ad(**venue_ad.dict())
    db_venue_ad.save()
    return db_venue_ad


def get_venue_ad(venue_ad_id: int):
    return models.Venue_Ad.filter(models.Venue_Ad.id == venue_ad_id).first()


def get_venue_ad_by_name(name: str):
    return models.Venue_Ad.filter(models.Venue_Ad.name == name).first()


def get_venue_ads(skip: int = 0, limit: int = 100):
    return list(models.Venue_Ad.select().offset(skip).limit(limit))


def delete_venue_ads(venue_ad_ids: List[int]):
    venue_ad_ids = list(venue_ad_ids)
    # print(artist_ad_ids)
    q = models.Venue_Ad.delete().where(models.Venue_Ad.id << venue_ad_ids)
    print(q)
    return q.execute()


def venue_ad_processer(props):
    # print(props)
    venue = get_venue_by_name(props.name)
    if venue is None:
        venue_dict = {"name": props.name, "photos": [props.photo], "address": props.city, "schedule": props.free_dates,
                      "contacts": props.contacts, "equipment": props.equipment, "have_soundguy": props.have_soundguy,
                      "have_lightguy": props.have_lightguy, "start_date": int(datetime.now().timestamp()),
                      "owner": 847266099681296385}
        venue = create_venue(schemas.VenueCreate.parse_obj(venue_dict))
    # solution 1 (easy)
    genre_list = []
    all_genres = get_genres()
    for genre in props.genres:
        if genre not in all_genres:
            genre = create_genre(schemas.GenreCreate.parse_obj({"name": genre}))
        else:
            genre = get_genre_by_name(genre)
        genre_list.append(genre.id)  # ?

    reqs = props.requirements
    req_list = [create_requirement(schemas.RequirementCreate.parse_obj(req)).id for req in reqs]
    # for req in reqs:
    #     r = create_requirement(schemas.RequirementCreate.parse_obj(req))
    #     req_list.append(r.id)
    venue_ad_dict = {"owner": 847266099681296385, "short_name": props.name, "text": props.description,
                     "requirements": req_list, "genres": genre_list, "date": props.free_dates[0], "status": "new",
                     "venue": venue.id}
    venue_ad = create_venue_ad(schemas.VenueAdCreate.parse_obj(venue_ad_dict))
    return venue_ad


async def process_venue_ad(venue_ad):
    ad_id = venue_ad.id
    name = venue_ad.short_name
    requirements = await get_requirements_from_list(venue_ad.requirements)
    genres = await get_genre_names_from_list(venue_ad.genres[:3] if len(venue_ad.genres) >= 3 else venue_ad.genres[:3])
    dt = venue_ad.date
    photo = venue_ad.venue.photos[0]
    city = venue_ad.venue.address
    venue_ad_dict = {
        "ad_id": ad_id,
        "type": "venue_ad",
        "name": name,
        "requirements": requirements,
        "genres": genres,
        "date": dt,
        "photo": photo,
        "city": city
    }
    return venue_ad_dict


async def get_all_venue_ads():
    venue_ads = get_venue_ads()
    ads = []
    tasks = [asyncio.create_task(process_venue_ad(venue_ad)) for venue_ad in venue_ads]
    ads = await asyncio.gather(*tasks)

    return ads


async def get_rendered_venue_ad(ad_id: int):
    venue_ad = get_venue_ad(ad_id)
    ad_id = venue_ad.id
    name = venue_ad.short_name
    requirements = await get_requirements_from_list(venue_ad.requirements)
    genres = await get_genre_names_from_list(venue_ad.genres)
    dt = venue_ad.date
    photo = venue_ad.venue.photos[0]
    description = venue_ad.text
    status = venue_ad.status
    equipment = venue_ad.venue.equipment
    contacts = venue_ad.venue.contacts
    city = venue_ad.venue.address
    venue_ad_dict = {"ad_id": ad_id, "name": name, "requirements": requirements,
                     "genres": genres, "date": dt, "photo": photo, "description": description,
                     "equipment": equipment, "status": status, "contacts": contacts, "city": city, "type": "artist_ad",
                     "have_soundguy": venue_ad.venue.have_soundguy, "have_lightguy": venue_ad.venue.have_lightguy}
    return venue_ad_dict


async def get_all_ads():
    t0 = time.time()
    tasks = [asyncio.create_task(get_all_artist_ads()), asyncio.create_task(get_all_venue_ads())]
    ads = await asyncio.gather(*tasks)
    t1 = time.time()
    print(t1 - t0)
    return ads[0] + ads[1]
