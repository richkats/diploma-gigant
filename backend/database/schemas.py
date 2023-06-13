# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any, List, Union

import peewee
from pydantic import BaseModel, validator
from pydantic.utils import GetterDict

from database import db_manager


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class DeleteResponseSchema(BaseModel):
    total: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# User schemas


class UserBase(BaseModel):
    first_name: str
    last_name: str
    nickname: str
    email: str
    photo: str


class UserDelete(BaseModel):
    user_ids: List[int]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# Genre schemas


class GenreBase(BaseModel):
    name: str


class GenreDelete(BaseModel):
    genre_ids: List[int]


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# Requirement schemas


class RequirementBase(BaseModel):
    name: str
    value: str


class RequirementDelete(BaseModel):
    requirement_ids: List[int]


class RequirementCreate(RequirementBase):
    pass


class Requirement(RequirementBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# Advertisement schemas


class AdvertisementBase(BaseModel):
    owner: Union[int, Any]
    short_name: str
    text: str
    requirements: List[int]
    genres: List[int]
    date: Union[datetime, int]
    status: str

    @validator("owner")
    def id_extract(cls, v):
        # print(type(v))
        if type(v) is db_manager.User:
            return int(v.id)
        elif type(v) is int:
            return v


class AdvertisementDelete(BaseModel):
    ad_ids: List[int]


class AdvertisementCreate(AdvertisementBase):
    pass


class Advertisement(AdvertisementBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# Artist schemas


class ArtistBase(BaseModel):
    name: str
    photos: List[bytes]
    city: str
    contacts: str
    start_date: Union[datetime, int]
    owner: Union[int, Any]

    @validator("owner")
    def id_extract(cls, v):
        # print(type(v))
        if type(v) is db_manager.User:
            return int(v.id)
        elif type(v) is int:
            return v


class ArtistDelete(BaseModel):
    artist_ids: List[int]


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# Artist_Ad schemas


class ArtistAdBase(AdvertisementBase):
    artist: Union[int, Any]
    city: str
    equipment: str

    @validator("artist")
    def artist_extract(cls, v):
        # print(type(v))
        if type(v) is db_manager.Artist:
            return int(v.id)
        elif type(v) is int:
            return v


class ArtistAdDelete(BaseModel):
    artist_ad_ids: List[int]


class ArtistAdCreate(ArtistAdBase):
    pass


class ArtistAdCreateProcess(BaseModel):
    name: str
    photo: bytes
    free_dates: List[int]
    requirements: List[dict]
    contacts: str
    genres: List[str]
    description: str
    equipment: str
    city: str


class ArtistAd(ArtistAdBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ShortArtistAd(BaseModel):
    ad_id: Any
    type: str
    name: str
    requirements: List[dict]
    genres: List[str]
    date: datetime
    photo: Any
    city: str

    @validator("photo")
    def photo_to_bytes(cls, v):
        # print(type(v))
        return bytes(v)

    @validator("ad_id")
    def ad_id_for_js(cls, v):
        return f"{v}"


class ArtistAdToRender(ShortArtistAd):
    description: str
    equipment: str
    status: str
    contacts: str


# Venue schemas


class VenueBase(BaseModel):
    name: str
    equipment: str
    address: str
    schedule: List[datetime]
    contacts: str
    have_soundguy: bool
    have_lightguy: bool
    start_date: Union[datetime, int]
    owner: Union[int, Any]
    photos: List[bytes]

    @validator("owner")
    def id_extract(cls, v):
        # print(type(v))
        if type(v) is db_manager.User:
            return int(v.id)
        elif type(v) is int:
            return v


class VenueDelete(BaseModel):
    venue_ids: List[int]


class VenueCreate(VenueBase):
    pass


class Venue(VenueBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# Venue_Ad schemas


class VenueAdBase(AdvertisementBase):
    venue: Union[int, Any]

    @validator("venue")
    def artist_extract(cls, v):
        # print(type(v))
        if type(v) is db_manager.Venue:
            return int(v.id)
        elif type(v) is int:
            return v


class VenueAdDelete(BaseModel):
    venue_ad_ids: List[int]


class VenueAdCreate(VenueAdBase):
    pass


class VenueAdCreateProcess(BaseModel):
    name: str
    photo: bytes
    free_dates: List[int]
    requirements: List[dict]
    contacts: str
    genres: List[str]
    have_soundguy: bool
    have_lightguy: bool
    description: str
    equipment: str
    city: str


class VenueAd(VenueAdBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class VenueAdToRender(ShortArtistAd):
    description: str
    equipment: str
    status: str
    contacts: str
    have_soundguy: bool
    have_lightguy: bool


class ShortVenueAd(BaseModel):
    ad_id: Any
    name: str
    requirements: List[dict]
    genres: List[str]
    date: datetime
    photo: Any
    type: str
    city: str

    @validator("photo")
    def photo_to_bytes(cls, v):
        return bytes(v)

    @validator("ad_id")
    def ad_id_for_js(cls, v):
        return f"{v}"
