
import webapp2

from google.appengine.api import memcache
from google.appengine.api import mail
from google.appengine.api import search
from google.appengine.ext.webapp.util import run_wsgi_app

import cgi
import json
import logging
import string
import urllib

# from models import Person

class Api(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("post")

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("get")

app = webapp2.WSGIApplication([
        ("/analysis/api", Api)
])
