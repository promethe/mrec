# check in on facebook
graph.put_object("me", "checkins", 
                    access_token=self.current_user.access_token,
                    message="Checked in with Kakapo!",
                    place=nearest_locations['data'][0]['id'],
                    coordinates="{\"latitude\":\"%f\", \"longitude\":\"%f\"}" % (latitude, longitude)
                    )

# find last checkin and put it in the database
lastCheckin = graph.get_connections("me", "checkins&limit=1")['data'][0]

checkin = Checkin.get_by_key_name(lastCheckin['id'])
if not checkin:    
    checkin = Checkin(key_name=str(lastCheckin['id']),
                        id=str(lastCheckin['id']),
                        owner=self.current_user,
                        location=db.GeoPt(latitude, longitude),
                        rating=1)
    checkin.put()
