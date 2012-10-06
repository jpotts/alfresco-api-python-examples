===Installation===

I strongly recommend you use virtualenv. Assuming you do that, the steps to install are:

1. Create a directory somewhere, suppose it is alfresco-oauth.
2. cd into alfresco-oauth and make a virtual environment by typing:
virtualenv env
3. Now activate your virtual environment by typing:
source ./env/bin/activate
4. This script requires oauth2client. The easiest way to install this is to type:
easy_install oauth2client

Now you're ready to configure your application key and secret.

===Configuration===

You need to know your Alfresco Cloud API key and secret. Go snag those and come back.

1. Edit client_secrets.json.sample.
2. For client_id, specify your API key
3. For client_secret, specify your secret
4. Leave everything else alone and save as client_secrets.json

If you are going to run cmis_create_document.py, you must edit the script to set:
NETWORK = 'alfresco.com'
SITE = 'alfresco-api-demo' # A site that already exists
FOLDER_NAME = 'test folder' # Name of a test folder to create
FILE = '/Users/jpotts/Documents/sample/sample-a.pdf' # Name of a file to upload
FILE_TYPE = 'application/pdf' # Mimetype of the file

===Running===

1. Execute the script
2. The script will invoke your default browser and ask you to grant access to the application.
3. After you grant access, the script will continue to run. The script currently spits out your home network and a list of sites in your home network.
4. The credential will be persisted to your keychain (untested on Windows!)
