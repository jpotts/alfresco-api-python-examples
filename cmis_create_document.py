#! /usr/bin/env python
import logging
from oauth2client.keyring_storage import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run
from httplib2 import Http
import json
from cmislib.model import CmisClient, CmisException
import os, pwd

NETWORK = 'alfresco.com'
SITE = 'alfresco-api-demo'
FOLDER_NAME = 'test folder'
FILE = '/Users/jpotts/Documents/sample/sample-a.pdf'
FILE_TYPE = 'application/pdf'

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

# Snag the user's home network
resp, content = http.request('https://api.alfresco.com')
networkList = json.loads(content)
homeNetwork = networkList['list']['entries'][0]['entry']['id']
print "Your home network appears to be: %s" % homeNetwork

headers = {'Authorization': 'Bearer ' + credentials.access_token}

client = CmisClient('https://api.alfresco.com/cmis/versions/1.0/atom',
                    '',
                    '',
                    headers=headers)
repo = client.defaultRepository

# Find the root folder of our target site
resp, content = http.request(
    'https://api.alfresco.com/%s/public/alfresco/versions/1/sites/%s/containers' %
    (NETWORK, SITE))
containerList = json.loads(content)
rootFolderId = containerList['list']['entries'][0]['entry']['id']

# Create a new folder in the root folder
rootFolder = repo.getObject(rootFolderId)

subFolder = None
try:
    subFolder = rootFolder.createFolder(FOLDER_NAME)
    print "Created folder: %s" % subFolder.id
except CmisException:
    path = rootFolder.getPaths()[0]
    subFolder = repo.getObjectByPath(path + '/' + FOLDER_NAME)
    print "Folder already existed"

# Like the folder
body = '{"id": "likes", "myRating": true}'
resp, content = http.request(
    'https://api.alfresco.com/%s/public/alfresco/versions/1/nodes/%s/ratings' %
    (NETWORK, subFolder.id),
    method='post',
    body=body)
print "You liked: %s" % subFolder.id

# Create a test document in the subFolder
file = open(FILE, 'rb')
fileName = file.name.split('/')[-1]
doc = None
try:
    doc = subFolder.createDocument(fileName, contentFile=file, contentType=FILE_TYPE)
    print "Created document: %s" % doc.id
except CmisException:
    path = subFolder.getPaths()[0]
    doc = repo.getObjectByPath(path + '/' + fileName)
    print "Document already existed: %s" % fileName
file.close()

# Create a comment on the test document
# NOTE: When dealing with documents, the REST API wants a versionSeriesID!
body = '{"content": "Here is a comment!"}'
resp, content = http.request(
    'https://api.alfresco.com/%s/public/alfresco/versions/1/nodes/%s/comments' %
    (NETWORK, doc.properties['cmis:versionSeriesId']),
    method='post',
    body=body)
print "You commented on: %s" % doc.id
