import csv
import datetime
import webapp2

from google.appengine.api import urlfetch

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


