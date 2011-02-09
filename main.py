#!/usr/bin/env python
#
# kakapo
# ------
# this file contains the kakapo core.
#
# (c) bogo giertler in '11

# system imports 
import os.path
import logging
import cgi

# GAE imports
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

# kakapo imports
from setup import *
from models import *
from venues import *
import facebook

class MainHandler(webapp.RequestHandler):
    @property
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = None
            cookie = facebook.get_user_from_cookie(self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
            if cookie:
                # store the information about the user in the datastore
                user = User.get_by_key_name(cookie["uid"])
                if not user:
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = User(key_name=str(profile["id"]),
                                id=str(profile["id"]),
                                name=profile["name"],
                                access_token=cookie["access_token"]
                                )
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                self._current_user = user
        
        memcache.set('current_user', self._current_user)
        return self._current_user                
    

class HomeHandler(MainHandler):
    def get(self):
        # logger.debug(self.nearest_locations("Pret", -0.1383, 51.5223))
        path = os.path.join(os.path.dirname(__file__), "templates/", "index.html")
        args = dict(current_user=self.current_user,
                    facebook_app_id=FACEBOOK_APP_ID)
        self.response.out.write(template.render(path, args))


class VenueHandler(webapp.RequestHandler):    
    def nearby_venues(self, longitude, latitude, name):
        current_user = memcache.get('current_user')
        
        if not hasattr(self, "_nearby_venues"):
            self._nearby_venues = None
            logger.debug("Starting nearby_venues")
            graph = facebook.GraphAPI(current_user.access_token)
            nearby_venues = graph.request("search",
                                                {"limit":10,
                                                "access_token":current_user.access_token,
                                                "q":name,
                                                "type":"place",
                                                "center": "%s,%s" % (latitude, longitude),
                                                "distance":"1000"
                                                })
            self._nearby_venues = nearby_venues['data']
        
        memcache.set('nearby_venues', self._nearby_venues)
        return self._nearby_venues
            
    def post(self):
        longitude = cgi.escape(self.request.get('longitude'))
        latitude = cgi.escape(self.request.get('latitude'))
        memcache.set('longitude', longitude)
        memcache.set('latitude', latitude)
        
        name = cgi.escape(self.request.get('venue_type'))
        
        logger.debug("%s, %s, %s", longitude, latitude, name)        
        path = os.path.join(os.path.dirname(__file__), "templates/", "venues.html")
        args = dict(nearby_venues = self.nearby_venues(longitude, latitude, name),
                    facebook_app_id=FACEBOOK_APP_ID)
        self.response.out.write(template.render(path, args))
        
        

class CheckinHandler(webapp.RequestHandler):
    def get(self):
        location = cgi.escape(self.request.get('location'))        
        current_user = memcache.get('current_user')
        longitude = memcache.get('longitude')
        latitude = memcache.get('latitude')
        
        logger.debug("%s, %s", longitude, latitude)
        
        graph = facebook.GraphAPI(current_user.access_token)
        
        graph.put_object("me", "checkins", 
                            access_token=current_user.access_token,
                            message="Checked in with Kakapo!",
                            place=location,
                            coordinates="{\"latitude\":\"%s\", \"longitude\":\"%s\"}" % (latitude, longitude)
                            )
        
        # find last checkin and put it in the database
        lastCheckin = graph.get_connections("me", "checkins&limit=1")['data'][0]

        checkin = Checkin.get_by_key_name(lastCheckin['id'])
        if not checkin:    
            checkin = Checkin(key_name=str(lastCheckin['id']),
                                id=str(lastCheckin['id']),
                                name=lastCheckin['place']['name'],
                                owner=current_user,
                                location=db.GeoPt(latitude, longitude),
                                rating=1)
            checkin.put()

        
        path = os.path.join(os.path.dirname(__file__), "templates/", "checkin.html")
        args = dict(checkin=checkin, facebook_app_id=FACEBOOK_APP_ID)
        self.response.out.write(template.render(path, args))
    

def main():
    application = webapp.WSGIApplication([('/', HomeHandler),
                                          ('/venues', VenueHandler),
                                          ('/checkin', CheckinHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
