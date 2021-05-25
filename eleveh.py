
from google.appengine.ext import ndb

# ElectricVehicle
#ELEVEH
# Modelfor ndb with its features

class ELEVEH(ndb.Model):
    name=ndb.StringProperty()
    manufacturer=ndb.StringProperty()
    year=ndb.IntegerProperty()
    batterySize=ndb.FloatProperty()
    WLTPRange=ndb.FloatProperty()
    cost=ndb.FloatProperty()
    power=ndb.FloatProperty()
    review=ndb.StringProperty(repeated=True)
    score=ndb.IntegerProperty(repeated=True)
