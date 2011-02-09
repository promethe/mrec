#!/usr/bin/env python
#
# kakapo
# ------
# this file contains data models for kakapo. all ids refer to the Fb OpenGraph ids.
#
# (c) bogo giertler in '11

from google.appengine.ext import db

class User(db.Model):
    ''' A user class that we use to manage the users within the kakapo '''
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    name = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)

# class Location(db.Model):

class Checkin(db.Model):
    ''' A checkin class that we use to manage the checkins within the kakapo '''
    id = db.StringProperty(required=True)
    name = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    owner = db.ReferenceProperty(User, required=True)
    location = db.GeoPtProperty(required=True)
    rating = db.RatingProperty(required=True)