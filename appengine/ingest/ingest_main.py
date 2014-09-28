
import webapp2

import cgi
import json
import logging
import string
import urllib

import ingest_chief_delphi

app = webapp2.WSGIApplication([
        ("/ingest/chiefdelphi", ingest_chief_delphi.GetNewData)
])
