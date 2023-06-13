# -*- coding: utf-8 -*-

from .credentials import *

from contextvars import ContextVar
import peewee as pw
from playhouse.cockroachdb import CockroachDatabase, ArrayField

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())

db = CockroachDatabase(COCKROACHDB_URL)


class PeeweeConnectionState(pw._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db._state = PeeweeConnectionState()


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):  # TODO: Done
    first_name = pw.CharField()
    last_name = pw.CharField()
    nickname = pw.CharField()
    password = pw.CharField()
    email = pw.CharField()
    photo = pw.BlobField()


class Requirement(BaseModel):  # TODO: Done
    #requirement_id = pw.PrimaryKeyField()
    name = pw.CharField()
    value = pw.CharField()


class Genre(BaseModel):  # TODO: Done
    #genre_id = pw.PrimaryKeyField()
    name = pw.CharField()


class Advertisement(BaseModel):  # TODO: Done
    #ad_id = pw.PrimaryKeyField()
    owner = pw.ForeignKeyField(User, backref="ads")
    short_name = pw.CharField()
    text = pw.CharField()
    requirements = ArrayField(pw.IntegerField)
    genres = ArrayField(pw.IntegerField)
    date = pw.DateTimeField()
    status = pw.CharField()


class Artist(BaseModel):  # TODO: Done
    name = pw.CharField()
    photos = ArrayField(pw.BlobField)
    city = pw.CharField()
    contacts = pw.CharField()
    start_date = pw.DateTimeField()
    owner = pw.ForeignKeyField(User, backref="artists")


class Venue(BaseModel):
    name = pw.CharField()
    equipment = pw.CharField()
    address = pw.CharField()
    schedule = ArrayField(pw.DateTimeField)
    contacts = pw.CharField()
    have_soundguy = pw.BooleanField()
    have_lightguy = pw.BooleanField()
    start_date = pw.DateTimeField()
    photos = ArrayField(pw.BlobField)
    owner = pw.ForeignKeyField(User, backref="venues")


class Artist_Ad(Advertisement):  # TODO: in process...
    artist = pw.ForeignKeyField(Artist)
    city = pw.CharField()
    equipment = pw.CharField()


class Venue_Ad(Advertisement):
    venue = pw.ForeignKeyField(Venue)


class Event(BaseModel):
    name = pw.CharField()
    description = pw.CharField()
    datetime = pw.DateTimeField()
    artists = ArrayField(pw.IntegerField)
    venue = pw.ForeignKeyField(Venue)
    photos = ArrayField(pw.BlobField)
    status = pw.CharField()


def create_tables():
    with db:
        db.create_tables(([User, Requirement, Genre, Artist, Venue, Artist_Ad, Venue_Ad, Event, Advertisement]))


def create_user(first_name: str, last_name: str, nickname: str, password: str, email: str, photo=None):
    if photo is None:
        photo = "default_photo"
    user = User.create(first_name=first_name, last_name=last_name, nickname=nickname, password=password, email=email, photo=photo)
    return user


def get_user_by_ib(user_id: int):
    user = User.get(id=user_id)
    return user


def delete_user(user_id: int):
    user = get_user_by_ib(user_id)
    user.delete()


def get_all_users():
    users = User.select()
    for user in users:
        print(user)


if __name__ == "__main__":
    # create_tables()
    with db:
        db.drop_tables([Event])
        db.drop_tables([Venue, Venue_Ad, Artist_Ad, Artist])
        db.create_tables([Venue, Venue_Ad, Artist_Ad, Artist, Event])
