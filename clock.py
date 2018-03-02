############
#LOCAL CODE#
############

#TODO: Make the sheet be in the cloud.
	#Convert from cloud to database for more reliable solution
	#Update fields to coordinate with the fields on the website
	#Get the CSV  parser to use UTF-8

import os
import sys
import json
import csv
import time
from datetime import datetime

import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
oldrefslist = []
newrefslist = []
dont_run_first = 0
read_in_sheet = {}

def send_message(recipient_id, message_text):
    params = {
        "access_token": "EAAEmOnlImrQBAOL0HonblqEoKiHnNQVcb1ykCH68cGgBuvkNMGsbgnYKQGagXou8EjunOrZCfI4soyqxPsmjlUkjoANN47UdVOgqu8FtbG6WvYYMHfHaaxVa4ZBmVFejdls3l7jGzp9BMKiuxi1enCUGkgjrZCSS4bZADhUeZAGYVunZAA2rbH"#os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
def getref(referralnum):
	#calls the list reflist which contains each of the referrals in dictionary form. Prints all the keys and dictionaries.
	#Accepts a int arguement to find a referral.
	return newrefslist[referralnum]
def getarea(referralnum):
	#calls the list reflist and accepts an int to find a referral than accesses the key value for that referrals location.	
	return newrefslist[referralnum]['Select-5']
def preprefsheet(dont_run_first):
	#Reads English referrals II
	#newrefslist = []#all referrals populated here
	with open('utf16file.csv', 'r', newline='', encoding='utf-16') as csvf:
	#Opens a document and formats it according to myDialect, assigns object to 'reader'
		engref2 = csv.DictReader(csvf, dialect='myDialect', quotechar='|')
		
		#Slay the ephemeral file system
		#####
		
		track_num = drive.CreateFile({'id':'1R7i_S2vtUQdhuJu2LdhKishtFrBSUYxd'})
		readnum = track_num.GetContentString()
		readnum = int(readnum)
		#####
		
		#Open the local file and get the left off on number, replace with file from drive.
		# with open('lastread.txt', 'r') as num:
			# readnum = num.read()
		# readnum = int(readnum)
		
		#gets where the program left off last  time
		escaped_start1 = readnum
		
		if dont_run_first == 1:
			newrefslist.clear()
			oldrefslist.clear()
		else:
			dont_run_first = 1
		
		for referral in engref2:# puts 100percent of referrals in newrefslist
			newrefslist.append(referral)
		for newref in newrefslist[readnum:]:#puts only the new referrals in oldrefslist
			oldrefslist.append(newref)
		#for oldref in newrefslist[:readnum]:#puts only the old referrals in oldrefslist
			#oldrefslist.append(oldref)
			
		#Write new number of referals to the file. Replace with drive.
		readnum = len(oldrefslist) + readnum
		
		readnum = str(readnum)
		track_num.SetContentString(readnum)
		track_num.Upload()
		readnum = int(readnum)
		
		# savenum = open('lastread.txt', 'w')
		# savenum.write(str(readnum))
		
		return {'1o':escaped_start1,'1n':readnum, 'rf':dont_run_first}
	
#TODO: Update  all of these to the fields that the actual Drive form uses. Add a source field.
def dict2ref(single_ref_dict):
	#Structures the referral into a message for missionaries
		#Argument must be a dictionary
	sub_date = str(single_ref_dict['Submitted On'])
	chin_name = str(single_ref_dict['Text-6'])
	eng_name = str(single_ref_dict['Text-8'])
	gender = str(single_ref_dict['Radio-2'])
	location = str(single_ref_dict['Select-5'])
	LINE = str(single_ref_dict['LINE ID'])
	phone = str(single_ref_dict['Text-9'])
	class_level = str(single_ref_dict['Radio-3'])
	comments = str(single_ref_dict['Textarea-10'])
	gospel = str(single_ref_dict['Radio-4'])
	sqfsource = str(single_ref_dict['Source'])
	ref = """Hello, you have a new referral.

Send date: %s
Chinese Name: %s
English Name: %s
Gender: %s
Location: %s
LINE ID: %s
Phone Number: %s
Class Level: %s
Questions, Comments, and Concerns: %s
Do they want the gospel?: %s
What campaign did they come from: %s
""" % (sub_date, chin_name, eng_name, gender, location, LINE, phone, class_level, comments, gospel, sqfsource)
	return ref

#AUTHENTICATION
#-------------------------------------------------------------------------------------------------------------------------------------------
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
#FILE ACCESS AND READING
#-------------------------------------------------------------------------------------------------------------------------------------------
folder_id = '1XhHfxaYUP_HDFSoIiP7ET63g3vSxcdpw' #<-Target folder to be read from, all docs in this folder will be read
lister = drive.ListFile({'q': "'%s' in parents" % folder_id}).GetList()
# ^ Vestigial ba.
refsheet = drive.CreateFile({'id':'1Q2xMx_TJwndYrEB2cyX4MK3dchMkvuUPPD6xuU4Osfw'}) #<-This doesnt make a new file in the drive
																			#rather it opens the document we are working with to be manipulated
refsheet.FetchMetadata()
refsheet.GetContentFile('utf8file.csv', mimetype='text/csv')
file_old = open('utf8file.csv', mode='r', encoding='utf-8')
file_new = open('utf16file.csv', mode='w', newline='', encoding='utf-16')
file_new.write(file_old.read())
file_old.close()
file_new.close()
download_mimetype = None
mimetypes = { 'application/vnd.google-apps.document': 'application/pdf',
	'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
#-------------------------------------------------------------------------------------------------------------------------------------------

sheet_one_dict = preprefsheet(dont_run_first)
dont_run_first = sheet_one_dict['rf']
readnuma = sheet_one_dict['1n']
escaped_start1a = sheet_one_dict['1o']

# print("readnuma %s" % (readnuma))
# print("escaped_start1a %s" % (escaped_start1a))


while escaped_start1a < readnuma:
	has_id = 0
	area_ct_num = 0
	message_text1a = getref(escaped_start1a)
	FB_text_1 = dict2ref(message_text1a)
	print(FB_text_1)
	read_in_sheet.clear()
	with open('EUL.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			key = 'area'
			read_in_sheet.setdefault(key, [])
			read_in_sheet[key].append(row['area'])
			key = 'sender_id'
			read_in_sheet.setdefault(key, [])
			read_in_sheet[key].append(row['sender_id'])
		csvfile.close()
	#pull ref recipient
	ww_num = len(read_in_sheet['area'])
	ww_num = ww_num - 1
	area = getarea(escaped_start1a)
	while has_id == 0:
		#make this drop out of loop if there at end of list  so it doesn't parse off the end
		area_cache = str(read_in_sheet['area'][area_ct_num])
		if area_cache == area:
			sender_id = int(read_in_sheet['sender_id'][area_ct_num])
			has_id = 1
		elif ww_num == area_ct_num and has_id == 0:
			#no id for a ref location
			sender_id = 1422808141175994
			has_id = 1
		else:
			area_ct_num = area_ct_num + 1
	send_message(sender_id, FB_text_1)
	escaped_start1a = escaped_start1a + 1