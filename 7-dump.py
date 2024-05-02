#!/usr/bin/python3
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


state = State(name="Califonia")
city = City(name="new City", state_id=state.id)
user = User(email="valentine@gmail.com", password="valentine")

place = Place(user_id=user.id, city_id=city.id, name="house")
amenity = Amenity(name="WiFi")
review = Review(user_id=user.id, place_id=place.id, text="good enough")

storage.new(state)
storage.new(city)
storage.new(user)
storage.new(place)
storage.new(amenity)
storage.new(review)
storage.save()

print("Okay")
