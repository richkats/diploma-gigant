# -*- coding: utf-8 -*-
import typing
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from database import db_manager as db, crud, schemas

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sleep_time = 10


async def reset_db_state():
    db.db._state._state.set(db.db_state_default.copy())
    db.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        db.db.connect()
        yield
    finally:
        if not db.db.is_closed():
            db.db.close()


# User API


@app.post("/users/", response_model=schemas.User, dependencies=[Depends(get_db)], tags=["User"])
async def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(user=user)


@app.get("/users/", response_model=List[schemas.User], dependencies=[Depends(get_db)], tags=["User"])
def read_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(skip=skip, limit=limit)
    return users


@app.delete("/users/", response_model=schemas.DeleteResponseSchema, dependencies=[Depends(get_db)], tags=["User"])
def delete_users(user_ids: schemas.UserDelete):
    return {"total": crud.delete_users(user_ids.user_ids)}


# Genre API


@app.post("/genres/", response_model=schemas.Genre, dependencies=[Depends(get_db)], tags=["Genre"])
async def create_genre(genre: schemas.GenreCreate):
    db_genre = crud.get_genre_by_name(name=genre.name)
    if db_genre:
        raise HTTPException(status_code=400, detail="Genre already exist")
    return crud.create_genre(genre=genre)


@app.get("/genres/", response_model=List[schemas.Genre], dependencies=[Depends(get_db)], tags=["Genre"])
async def read_genres(skip: int = 0, limit: int = 100):
    genres = crud.get_genres(skip=skip, limit=limit)
    return genres


@app.delete("/genres/", response_model=schemas.DeleteResponseSchema, dependencies=[Depends(get_db)], tags=["Genre"])
def delete_genres(genre_ids: schemas.GenreDelete):
    return {"total": crud.delete_genres(genre_ids.genre_ids)}


# Requirement API


@app.post("/requirements/", response_model=schemas.Requirement, dependencies=[Depends(get_db)], tags=["Requirement"])
async def create_requirement(requirement: schemas.RequirementCreate):
    # db_requirement = crud.get_requirement_by_name(name=requirement.name)
    # if db_requirement:
    #     raise HTTPException(status_code=400, detail="Requirement already exist")
    return crud.create_requirement(requirement=requirement)


@app.get("/requirements/", response_model=List[schemas.Requirement], dependencies=[Depends(get_db)],
         tags=["Requirement"])
async def read_requirements(skip: int = 0, limit: int = 100):
    requirements = crud.get_requirements(skip=skip, limit=limit)
    return requirements


@app.delete("/requirements/", response_model=schemas.DeleteResponseSchema, dependencies=[Depends(get_db)],
            tags=["Requirement"])
def delete_requirements(requirement_ids: schemas.RequirementDelete):
    return {"total": crud.delete_requirements(requirement_ids.requirement_ids)}


# Advertisement API


@app.post("/advertisements/", response_model=schemas.Advertisement, dependencies=[Depends(get_db)],
          tags=["Advertisement"])
async def create_advertisement(ad: schemas.AdvertisementCreate):
    # db_requirement = crud.get_requirement_by_name(name=requirement.name)
    # if db_requirement:
    #     raise HTTPException(status_code=400, detail="Requirement already exist")
    return crud.create_advertisement(ad=ad)


@app.get("/advertisements/", response_model=List[schemas.Advertisement], dependencies=[Depends(get_db)],
         tags=["Advertisement"])
async def read_advertisements(skip: int = 0, limit: int = 100):
    ads = crud.get_advertisements(skip=skip, limit=limit)
    return ads


@app.delete("/advertisements/", response_model=schemas.DeleteResponseSchema, dependencies=[Depends(get_db)],
            tags=["Advertisement"])
def delete_advertisement(ad_ids: schemas.AdvertisementDelete):
    return {"total": crud.delete_advertisement(ad_ids.ad_ids)}


# Artist API


@app.post("/artists/", response_model=schemas.Artist, dependencies=[Depends(get_db)], tags=["Artist"])
async def create_artist(artist: schemas.ArtistCreate):
    # db_requirement = crud.get_requirement_by_name(name=requirement.name)
    # if db_requirement:
    #     raise HTTPException(status_code=400, detail="Requirement already exist")
    return crud.create_artist(artist=artist)


@app.get("/artists/", response_model=List[schemas.Artist], dependencies=[Depends(get_db)], tags=["Artist"])
async def read_artists(skip: int = 0, limit: int = 100):
    artists = crud.get_artists(skip=skip, limit=limit)
    return artists


@app.delete("/artists/", response_model=schemas.DeleteResponseSchema, dependencies=[Depends(get_db)], tags=["Artist"])
def delete_artist(artist_ids: schemas.ArtistDelete):
    return {"total": crud.delete_artist(artist_ids.artist_ids)}


# Artist Ad API


@app.post("/artist_ads/", response_model=schemas.ArtistAd, dependencies=[Depends(get_db)], tags=["Artist Ad"])
async def create_artist_ad(artist_ad: schemas.ArtistAdCreate):
    # db_requirement = crud.get_requirement_by_name(name=requirement.name)
    # if db_requirement:
    #     raise HTTPException(status_code=400, detail="Requirement already exist")
    return crud.create_artist_ad(artist_ad=artist_ad)


@app.get("/artist_ads/", response_model=List[schemas.ArtistAd], dependencies=[Depends(get_db)], tags=["Artist Ad"])
async def read_artist_ads(skip: int = 0, limit: int = 100):
    artist_ads = crud.get_artist_ads(skip=skip, limit=limit)
    return artist_ads


@app.delete("/artist_ads/", response_model=schemas.DeleteResponseSchema, dependencies=[Depends(get_db)],
            tags=["Artist Ad"])
def delete_artist_ad(artist_ad_ids: schemas.ArtistAdDelete):
    return {"total": crud.delete_artist_ad(artist_ad_ids.artist_ad_ids)}


@app.post("/create_artist_ad/", response_model=schemas.ArtistAd, dependencies=[Depends(get_db)], tags=["Artist Ad"])
async def create_new_artist_ad(props: schemas.ArtistAdCreateProcess):
    return crud.artist_ad_processer(props)


@app.get("/all_artist_ads/", response_model=List[schemas.ShortArtistAd], dependencies=[Depends(get_db)],
         tags=["Artist Ad"])
async def get_all_artist_ads():
    return await crud.get_all_artist_ads()


@app.get("/rendered_artist_ad/", response_model=schemas.ArtistAdToRender, dependencies=[Depends(get_db)],
         tags=["Artist Ad"])
async def get_rendered_artist_ad(ad_id: str):
    return await crud.get_rendered_artist_ad(int(ad_id))


# Venue API


@app.post("/venues/", response_model=schemas.Venue, dependencies=[Depends(get_db)], tags=["Venue"])
async def create_venue(venue: schemas.VenueCreate):
    return crud.create_venue(venue=venue)


@app.get("/venues/", response_model=List[schemas.Venue], dependencies=[Depends(get_db)], tags=["Venue"])
async def read_venues(skip: int = 0, limit: int = 100):
    venues = crud.get_venues(skip=skip, limit=limit)
    return venues


@app.delete("/venues/", response_model=schemas.DeleteResponseSchema, dependencies=[Depends(get_db)], tags=["Venue"])
def delete_artist(venue_ids: schemas.VenueDelete):
    return {"total": crud.delete_venues(venue_ids.venue_ids)}


# Venue Ad API


@app.post("/venue_ads/", response_model=schemas.VenueAd, dependencies=[Depends(get_db)], tags=["Venue Ad"])
async def create_venue_ad(venue_ad: schemas.VenueAdCreate):
    return crud.create_venue_ad(venue_ad=venue_ad)


@app.get("/venue_ads/", response_model=List[schemas.VenueAd], dependencies=[Depends(get_db)], tags=["Venue Ad"])
async def read_venue_ads(skip: int = 0, limit: int = 100):
    venue_ads = crud.get_venue_ads(skip=skip, limit=limit)
    return venue_ads


@app.delete("/venue_ads/", response_model=schemas.DeleteResponseSchema, dependencies=[Depends(get_db)],
            tags=["Venue Ad"])
def delete_artist(venue_ad_ids: schemas.VenueAdDelete):
    return {"total": crud.delete_venue_ads(venue_ad_ids.venue_ad_ids)}


@app.post("/create_venue_ad/", response_model=schemas.VenueAd, dependencies=[Depends(get_db)], tags=["Venue Ad"])
async def create_new_venue_ad(props: schemas.VenueAdCreateProcess):
    return crud.venue_ad_processer(props)


@app.get("/all_venue_ads/", response_model=List[schemas.ShortVenueAd], dependencies=[Depends(get_db)],
         tags=["Venue Ad"])
async def get_all_venue_ads():
    return await crud.get_all_artist_ads()


@app.get("/rendered_venue_ad/", response_model=schemas.VenueAdToRender, dependencies=[Depends(get_db)],
         tags=["Venue Ad"])
async def get_rendered_venue_ad(ad_id: str):
    return await crud.get_rendered_venue_ad(int(ad_id))


@app.get("/all_ads/", response_model=List[schemas.ShortVenueAd], dependencies=[Depends(get_db)], tags=["Ads"])
async def get_all_ads():
    return await crud.get_all_ads()


# Test route


@app.post("/")
async def index(request: Request):
    # print(request.json())
    return await request.form()
