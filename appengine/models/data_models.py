from google.appengine.api import users
from google.appengine.ext import ndb
import string
import random
import sys

# A class to store a mapping from a score type to the score. Score types might be:
# Autonomous, Hybrid, Teleoperated, Endgame, Foul, Total Score, etc.
class ScoreEntry(ndb.Model):
    score_type = ndb.StringProperty(indexed=False)
    score = ndb.IntegerProperty(indexed=False)



# An entry containing data for one alliance (if team_number is None) or one team in one match.
# Data can come from any source, including a human
class DataEntry(ndb.Model):
    # Where the data came from
    source = ndb.StringProperty(indexed=True)
    time_collected = ndb.DateTimeProperty(auto_now=True,indexed=False)
    
    # Identifying features
    # TODO do we need to index everything? Can we just use match number perhaps?
    year = ndb.DateTimeProperty(indexed=True)
    event = ndb.StringProperty(indexed=True)
    match_number = ndb.IntegerProperty(indexed=True)
    match_time = ndb.DateTimeProperty(indexed=False)
    alliance = ndb.IntegerProperty(indexed=True)
    team_number = ndb.IntegerProperty(indexed=True)
    teamsPlayed = ndb.IntegerProperty(indexed=False,repeated=True)

    # Data
    scores = ndb.StructuredProperty(ScoreEntry, repeated=True)
