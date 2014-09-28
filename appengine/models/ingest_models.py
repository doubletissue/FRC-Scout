from google.appengine.api import users
from google.appengine.ext import ndb
import string
import random
import sys

# A Data Source defines a location to pull data from. Each source should
# extend this class and implement the collect function, which will get 
# any new data, and the shouldCollect function, which will determine if
# the source should be collected from again. The data will be stored in the
# "data" member to be processed in the future via task queues in the parse 
# function
class DataSource(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    last_collected = ndb.DateTimeProperty(indexed=True)
    uri = ndb.StringProperty(indexed=False)
    data = ndb.JsonProperty(compressed=True)

    def collect(self):
        raise NotImplementedError

    def shouldCollect(self):
        raise NotImplementedError

    def parse(self):
        raise NotImplementedError

