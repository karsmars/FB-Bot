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


newreferrals = []
referrallist = []
dont_run_first = 0
read_in_sheet = {}
googlerefsheet = drive.CreateFile({'id':'1Q2xMx_TJwndYrEB2cyX4MK3dchMkvuUPPD6xuU4Osfw'}) #<-This doesnt make a new file in the drive
																			#rather it opens the document we are working with to be manipulated
googlerefsheet.FetchMetadata()
googlerefsheet.GetContentFile('googlerefsheet.csv', mimetype='text/csv')
referrals = open('googlerefsheet.csv', "r", encoding='utf-8')
csvrefsheet = csv.DictReader(referrals)


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
	#uses the provided integer to call a referral from the list referrallist by its indice
	return referrallist[referralnum]
def getarea(referralnum):
	#uses the provided integer to call a referral's area from the list referrallist by its indice
	return referrallist[referralnum]['Select-5']
def preprefsheet(dont_run_first):
	track_num = drive.CreateFile({'id':'1R7i_S2vtUQdhuJu2LdhKishtFrBSUYxd'})
	readnum = track_num.GetContentString()
	readnum = int(readnum)
	#gets where the program left off last  time
	escaped_start1 = readnum
	if dont_run_first == 1:
		referrallist.clear()
		newreferrals.clear()
	else:
		dont_run_first = 1
	#THIS for loop is to make a list that serves as a complete library of all referrals 
	for referral in csvrefsheet:# puts 100percent of referrals in referrallist to be manipulated by dict2ref
		referrallist.append(referral)
	#AND THIS for loop is for counting how many of the referrals are new compared to last time and recording that amount
	for newref in referrallist[readnum:]:#puts only the new referrals in newreferrals so that they can be counted and added to readnum then uploaded to gdrive as track_num
		newreferrals.append(newref)
	#Write new number of referrals to a track_num and throw it up into drive
	readnum = len(newreferrals) + readnum
	readnum = str(readnum)
	track_num.SetContentString(readnum)
	track_num.Upload()
	readnum = int(readnum)
	return {'1o':escaped_start1,'1n':readnum, 'rf':dont_run_first}
def dict2ref(single_ref_dict):
	#Structures the referral into a message for missionaries
		#Argument must be a dictionary
	#Pull dictionaries 
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
	
	if phone == '0':
		phone = 'No phone number provided.'
	else:
		phone = '0' + phone
	
	line_lower = LINE.lower()
	if 'a' not in line_lower and 'b' not in line_lower and 'c' not in line_lower and 'd' not in line_lower and 'e' not in line_lower and 'f' not in line_lower and 'g' not in line_lower and 'h' not in line_lower and 'i' not in line_lower and 'j' not in line_lower and 'k' not in line_lower and 'l' not in line_lower and 'm' not in line_lower and 'n' not in line_lower and 'o' not in line_lower and 'p' not in line_lower and 'q' not in line_lower and 'r' not in line_lower and 's' not in line_lower and 't' not in line_lower and 'u' not in line_lower and 'v' not in line_lower and 'w' not in line_lower and 'x' not in line_lower and 'y' not in line_lower and 'z' not in line_lower:
		if len(line_lower) == 9:
			LINE = '0' + LINE
	#Compile the referral
	ref = """Hello, you have a new referral. Make sure you contact this person as soon as possible.
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
What source did they come from?: %s
""" % (sub_date, chin_name, eng_name, gender, location, LINE, phone, class_level, comments, gospel, sqfsource)
	return ref
	#print(ref)
# for ref in csvrefsheet:
	# dict2ref(ref)
sheet_one_dict = preprefsheet(dont_run_first)
dont_run_first = sheet_one_dict['rf']
readnuma = sheet_one_dict['1n']
escaped_start1a = sheet_one_dict['1o']

# print("readnuma %s" % (readnuma))
# print("escaped_start1a %s" % (escaped_start1a))

while escaped_start1a < readnuma:
	has_id = 0
	area_ct_num = 0
	is_default = 0
	message_text1a = getref(escaped_start1a)
	FB_text_1 = dict2ref(message_text1a)
	print(FB_text_1)
	read_in_sheet.clear()
	#Download the CSV file from the cloud
	eul_sheet = drive.CreateFile({'id':'15nNIEKubHxVFnVkxk_mkFRBPmmuHHHMp_E-rpU9OrAQ'})
	eul_sheet.GetContentFile('EUL_LIST.csv', mimetype='text/csv')
	#Parse the CSV file
	with open('EUL_LIST.csv', newline='') as csvfile:
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
			is_default = 1
		else:
			area_ct_num = area_ct_num + 1
	send_message(sender_id, FB_text_1)
	if is_default == 1:
		send_message(1422808141175994, 'This is not for your area.')
	escaped_start1a = escaped_start1a + 1
		
referrals.close()