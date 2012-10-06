#! /usr/bin/env python
import logging
from oauth2client.keyring_storage import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run
from httplib2 import Http
import json
from cmislib.model import CmisClient
import os, pwd

uid = pwd.getpwuid(os.getuid())[0]
storage = Storage("Jeff's Sample Python App", uid)
http = Http(disable_ssl_certificate_validation=True) # Should not have to do this!
flow = flow_from_clientsecrets('client_secrets.json',
                               scope='public_api',
                               redirect_uri='http://localhost:8080/')

credentials = storage.get()
if credentials == None:
    credentials = run(flow, storage, http=http)
    storage.put(credentials)

print "Your access_token is: %s" % credentials.access_token

http = credentials.authorize(http)

headers = {'Authorization': 'Bearer ' + credentials.access_token}

client = CmisClient('https://api.alfresco.com/cmis/versions/1.0/atom', '', '', headers=headers)
repo = client.defaultRepository
print "cmislib connected to:"
print "    Name: %s" % repo.getRepositoryInfo()['repositoryId']
print "  Vendor: %s" % repo.getRepositoryInfo()['vendorName']
print " Version: %s" % repo.getRepositoryInfo()['productVersion']
