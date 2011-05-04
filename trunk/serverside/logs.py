# Copyright (C) 2011, CloudCaptive
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import cgi
import logging
import os
import wsgiref.handlers
import urllib
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
from serverside import constants
from serverside import environment
from serverside.dao import logs_dao
from serverside.dao import passphrase_dao 

class LogEvent(webapp.RequestHandler):
  def post(self):
    logsecret = self.request.get('key') 
    official_log_secret = passphrase_dao.get_log_secret()    
    if logsecret != official_log_secret:
      logging.error("Logging: Bad logging secret: %s vs %s"%(logsecret, official_log_secret))
      return
    eventtype = self.request.get('event')
    if eventtype not in constants.LOGGING.CLIENT_EVENT and \
       eventtype not in constants.LOGGING.API_EVENT:
      logging.error("Unknown event type: %s"%eventtype)
      return
    diction = {}
    for args in self.request.arguments():
      diction[args] = self.request.get(args)
    logs_dao.save_log(diction)
    return 
    #logs_dao.save_log(newlog)
application = webapp.WSGIApplication([
  (constants.LOGGING.PATH, LogEvent)
], debug=constants.DEBUG)

def __url_async_post(url, argsdic):
  # This will not work on the dev server for GAE, dev server only uses
  # synchronous calls, unless the SDK is patched, or using AppScale
  rpc = urlfetch.create_rpc(deadline=10)
  urlfetch.make_fetch_call(rpc, url, payload=urllib.urlencode(argsdic), method=urlfetch.POST)

def full_path(relative_url):
  if environment.is_dev():
    return constants.DEV_URL + constants.LOGGING.PATH
  else:
    return constants.PRODUCTION_URL + constants.LOGGING.PATH

def create(diction):
  diction['key'] = passphrase_dao.get_log_secret()    
  assert ('event' in diction), "Logs must always have an event type"
  __url_async_post(full_path(constants.LOGGING.PATH), diction)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()