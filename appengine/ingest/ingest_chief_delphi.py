import csv
import datetime
import webapp2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from google.appengine.ext.ndb import query

import sys

from models import ingest_models
from models import data_models

CHIEF_DELPHI_URL = 'http://www.chiefdelphi.com/forums/frcspy.php?xml=csv'
CHIEF_DELPHI_ID = 'chief_delphi'


class ChiefDelphiDataSource(ingest_models.DataSource):
    def collect(self):
        result = urlfetch.fetch(self.uri)
        if result.status_code == 200:
            self.data = [result.content]
            self.last_collected = datetime.datetime.now()
        self.put()

    def shouldCollect(self):
        if not self.last_collected:
            return True
        return (datetime.datetime.now()-self.last_collected).seconds > 60

    def parse(self):
        pass

class GetNewData(webapp2.RequestHandler):
    def getNewData(self):
         dataSource = ChiefDelphiDataSource.get_by_id(CHIEF_DELPHI_ID)
         if not dataSource:
             dataSource = ChiefDelphiDataSource(id=CHIEF_DELPHI_ID, name=CHIEF_DELPHI_ID,uri=CHIEF_DELPHI_URL)
         if dataSource.shouldCollect():
             dataSource.collect()
             return True
         return False
         

    def post(self):
        t = self.getNewData()
        self.response.headers['Content-Type'] = 'text/plain'
        # string = str(urllib.unquote(cgi.escape(self.request.get('q')).lower()[:100]))
        self.response.out.write("post" + str(t))

    def get(self):
        t = self.getNewData()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("get" + str(t))

class ParseData(webapp2.RequestHandler):
    def parseData(self):
        data_source = ChiefDelphiDataSource.get_by_id(CHIEF_DELPHI_ID)
        if not data_source or not data_source.data:
            return 0
        data = str(data_source.data[0]).split('\n')
        reader = csv.DictReader(data[1:],fieldnames=data[0].split(','))
        data_list = list(reader)
        num_rows = len(data_list)

        last_entry = data_models.DataEntry.query(data_models.DataEntry.source==CHIEF_DELPHI_ID)
        last_entry = last_entry.order(-data_models.DataEntry.match_time)
        last_entry = last_entry.fetch(1)
        if len(last_entry) > 0:
            last_entry = last_entry[0]
        
        offset = 0
        if last_entry:
            last_time = last_entry.match_time
            while offset < num_rows:
                # Hack because not all systems support the offset
                date_str = data_list[offset]['date'].replace(' +0000','')
                match_time = datetime.datetime.strptime(date_str,'%a, %d %b %Y %H:%M:%S')
                if match_time <= last_time:
                    break
                offset += 1
        else:
            offset = len(data_list)
        entries = []
        for rowNum in range(offset-1,-1,-1):
            entry = data_list[rowNum]
            date_str = entry['date'].replace(' +0000','')
            match_time = datetime.datetime.strptime(date_str,'%a, %d %b %Y %H:%M:%S')
            points = {}
            for color in 'rb':
                for score_type in ['fpts','hpts','tpts']:
                    points[color+score_type] = int(entry[color+score_type])
                points[color+'spts'] = points[color+'tpts'] + points[color+'hpts']
                points[color+'epts'] = 0
            for alliance in ['red','blue']:
                foul_points = int(entry[alliance[0]+'fpts'])
                hybrid_points = int(entry[alliance[0]+'hpts'])
                teleop_points = int(entry[alliance[0]+'tpts'])
                scored_points = hybrid_points + teleop_points
                total_points = scored_points + foul_points
                fouls_earned = int(entry[('b' if alliance == 'red' else 'r') + 'fpts'])
                entries.append(data_models.DataEntry(source = CHIEF_DELPHI_ID,
                                                     year = int(match_time.year),
                                                     event = entry['event'],
                                                     match_number = int(entry['match']),
                                                     match_time = match_time,
                                                     alliance = 1 if alliance == 'red' else 0,
                                                     team_number = None,
                                                     teamsPlayed = [int(entry[alliance+i]) for i in ['1','2','3']],
                                                     scores = points
                                                     )
                               )
            if len(entries) >= 100:
                ndb.put_multi(entries)
                entries = []
                    
        ndb.put_multi(entries)
        return offset
        

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        t = self.parseData()
        # string = str(urllib.unquote(cgi.escape(self.request.get('q')).lower()[:100]))
        self.response.out.write("post" + str(t))

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        t = self.parseData()
        self.response.out.write("get" + str(t))
