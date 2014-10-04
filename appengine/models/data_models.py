from google.appengine.api import users
from google.appengine.ext import ndb
import string
import random
import sys

# A class to store a mapping from a score type to the score. Score types might be:
# Autonomous, Hybrid, Teleoperated, Endgame, Foul, Total Score, etc.
class ScoreEntry(ndb.Model):
    score_type = ndb.StringProperty(indexed=False,choices=['hyb_pts','tel_pts','scr_pts','tot_pts','f_gain_pts','f_gave_pts'])
    score = ndb.IntegerProperty(indexed=False)



# An entry containing data for one alliance (if team_number is None) or one team in one match.
# Data can come from any source, including a human
class DataEntry(ndb.Model):
    # Where the data came from
    source = ndb.StringProperty(indexed=True)
    time_collected = ndb.DateTimeProperty(auto_now=True,indexed=False)
    
    # Identifying features
    # TODO do we need to index everything? Can we just use match number perhaps?
    year = ndb.IntegerProperty(indexed=True)
    event = ndb.StringProperty(indexed=True)
    match_number = ndb.IntegerProperty(indexed=False)
    match_time = ndb.DateTimeProperty(indexed=True)
    alliance = ndb.IntegerProperty(indexed=True)
    team_number = ndb.IntegerProperty(indexed=True)
    teamsPlayed = ndb.IntegerProperty(indexed=True,repeated=True)

    # Data
    scores = ndb.JsonProperty()
    # scores = ndb.StructuredProperty(ScoreEntry, repeated=True)
