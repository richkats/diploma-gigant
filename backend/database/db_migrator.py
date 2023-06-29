# -*- coding: utf-8 -*-

from credentials import *
from playhouse.shortcuts import model_to_dict
from contextvars import ContextVar
import peewee as pw
from playhouse.cockroachdb import CockroachDatabase, ArrayField
import db_manager as old_db
import schemas

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())

db = CockroachDatabase(MIGRATE_URL)


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
    new_tables = [User, Requirement, Genre, Artist, Venue, Artist_Ad, Venue_Ad, Advertisement]
    db_schemas = [schemas.User, schemas.Requirement, schemas.Genre, schemas.Artist, schemas.Venue, schemas.ArtistAd, schemas.VenueAd, schemas.Advertisement]
    old_tables = [old_db.User, old_db.Requirement, old_db.Genre, old_db.Artist, old_db.Venue, old_db.Artist_Ad, old_db.Venue_Ad, old_db.Advertisement]
    for i, table in enumerate(old_tables):
        def setter(item):
            model_dict = model_to_dict(item)
            model_keys = list(model_dict.keys())
            model_values = list(model_dict.values())
            for j, value in enumerate(model_values):
                if type(value) is dict:
                    # print(model_values[j])
                    model_values[j] = value["id"]
            new_model = {}
            for j, value in enumerate(model_values):
                new_model[model_keys[j]] = value
            # new_model = dict.fromkeys(model_keys, model_values)
            print(new_model)
            new_instance = new_tables[i](**new_model)
            print(new_instance)
            new_instance.save(force_insert=True)
            db.commit()

        old_instances = list(table.select())
        for old_instance in old_instances:
            # print(model_to_dict(old_instance))
            # new_instance = new_tables[i](**model_to_dict(old_instance))
            # new_instance.save()
            setter(old_instance)
    # print(Genre.get())

    db.close()

    # create_tables()

    # with db:
    #     db.drop_tables([Event])
    #     db.drop_tables([Venue, Venue_Ad, Artist_Ad, Artist])
    #     db.create_tables([Venue, Venue_Ad, Artist_Ad, Artist, Event])
