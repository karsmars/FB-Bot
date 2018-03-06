import os
import sys
import json
import csv
import time
from datetime import datetime

import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("credentials.json")
if gauth.credentials is None:
	# Authenticate if they're not there   0auth2
	#gauth.LocalWebserverAuth()
	gauth.CommandLineAuth()
elif gauth.access_token_expired:
	# Refresh them if expired
	gauth.Refresh()
else:
	#Initialize the saved creds
	gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("credentials.json")
drive = GoogleDrive(gauth)

file_a = drive.CreateFile({'id':'1R7i_S2vtUQdhuJu2LdhKishtFrBSUYxd'})

#download the file
content = file_a.GetContentString()

#Turn  it into a number
number = int(content)
print('The old number is: %s' % (number))

#Set the number
number = input('Enter the number you want to set the file contents to: ')

#reupload the file
number = str(number)
file_a.SetContentString(number)
file_a.Upload()