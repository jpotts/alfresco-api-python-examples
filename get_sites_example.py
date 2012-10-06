#! /usr/bin/env python
import logging
from oauth2client.keyring_storage import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run
from httplib2 import Http
import json
import os, pwd

uid = pwd.getpwuid( os.getuid() )[ 0 ]
storage = Storage("Jeff's Sample Python App", uid)

http = Http(disable_ssl_certificate_validation=True) # Should not have to do this!
flow = flow_from_clientsecrets('client_secrets.json',
                               scope='public_api',
                               redirect_uri='http://localhost:8080/')

credentials = storage.get()
if credentials == None:
    credentials = run(flow, storage, http=http)
    storage.put(credentials)

print "access_token:" + credentials.access_token

http = credentials.authorize(http)

# Snag the user's home network
resp, content = http.request('https://api.alfresco.com')
networkList = json.loads(content)
homeNetwork = networkList['list']['entries'][0]['entry']['id']
print "Your home network appears to be: %s" % homeNetwork

# Find out what sites the user can see in his home network
resp, content = http.request('https://api.alfresco.com/%s/public/alfresco/versions/1/sites?maxItems=10' % homeNetwork)
siteList = json.loads(content)
for entry in siteList['list']['entries']:
    print "Site ID:%s" % entry['entry']['id']
