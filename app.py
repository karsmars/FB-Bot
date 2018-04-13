#############
#SERVER CODE#
#############

#TODO: Add a class level fill field to the register command.

#Library imports.
import os
import sys
import json
import csv
import time
from datetime import datetime

#Installed library imports.
import requests
from flask import Flask, request, jsonify
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#initialize Flask app
app = Flask(__name__)

#Define the GET route for the webhook.
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "elder_christiansen_was_here":#os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200
	
#Define the POST route for the webhook
@app.route('/', methods=['POST'])
def webhook():

	#Pull in the json sent by the POST request
	data = request.get_json()

	if data["object"] == "page":

		for entry in data["entry"]:
			for messaging_event in entry["messaging"]:
				if messaging_event.get("message"): # someone sent us a message
					if "text" not in messaging_event["message"].keys():
						return "Not a text message", 200
						pass
					else:
						sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending the message
						recipient_id = messaging_event["recipient"]["id"]  # our facebook ID number
						message_text = messaging_event["message"]["text"]  # the message's text
						#lowercase message text so we don't have to care about capitalization
						message_text = message_text.lower()
						
						#variable that triggers the default response if nobody 
						ignore_else = 0
						
						#TODO: Have users agree to receiving subscription messages.
						
						#check for and send a general help message
						# send_message(sender_id, '''Hello and welcome! I am Ricardo the facebook referral bot. I can help you do 4 things:
						# Register to recieve referrals for an area- type: "register(insert transfer password here)(insert your area name here)"
						# Display a help message- type "help"
						# Display a list of all the available areas- type "area list"
						# Unsubscribe you from recieving referrals- type "unsubscribe(insert area name here)"
						# Which can I do for you?''')
						
						# if 'info' in message_text:
							# if 'update' in message_text:
								# only_one, area = which_area(message_text)
								# if only_one == 0:
									# send_message(sender_id, 'No valid area name detected, please type "Area List" for a list of areas you can unsubscribe from.')
								# elif only_one == 1:
									# gauth = GoogleAuth()
									# Try to load saved client credentials
									# gauth.LoadCredentialsFile("credentials.json")
									# if gauth.credentials is None:
										# Authenticate if they're not there   0auth2
										# gauth.LocalWebserverAuth()
									# elif gauth.access_token_expired:
										# Refresh them if expired
										# gauth.Refresh()
									# else:
										#Initialize the saved creds
										# gauth.Authorize()
									# Save the current credentials to a file
									# gauth.SaveCredentialsFile("credentials.json")
									# drive = GoogleDrive(gauth)
									##auth complete###
									# areainfobotsheet = drive.CreateFile({'id':'1Prra8o6HXS2R6H1fq_4e1IZh4bB2O8WobA9mCy8V-j4'})
									# areainfobotsheet.FetchMetadata()
									# areainfobotsheet.GetContentFile('area_info.csv', mimetype='text/csv')
									# areafile = open('area_info.csv', 'r', encoding='utf-8')
									# areareader = csv.reader(areafile)
									 
								# elif only_one == 2:
									# send_message(sender_id, 'It looks you have made a mistake while trying to update info about a area and accidentally entered more than one area. Please enter only one area at a time.')
								# else:
									# send_message(sender_id, 'You were never supposed to see this message. A serious error has occured. Please contact boyd.christiansen on LINE immediately.')
								#send_message(sender_id, "Updating class information from the bot has not yet been built. Please message boyd.christiansen on LINE.")
							# else:
								# only_one, area = which_area(message_text)
								# if only_one == 0:
									# send_message(sender_id, 'No valid area name detected, please type "Area List" for a list of areas you can unsubscribe from.')
								# elif only_one == 1:
									# gauth = GoogleAuth()
									# Try to load saved client credentials
									# gauth.LoadCredentialsFile("credentials.json")
									# if gauth.credentials is None:
										# Authenticate if they're not there   0auth2
										# gauth.LocalWebserverAuth()
									# elif gauth.access_token_expired:
										# Refresh them if expired
										# gauth.Refresh()
									# else:
										#Initialize the saved creds
										# gauth.Authorize()
									# Save the current credentials to a file
									# gauth.SaveCredentialsFile("credentials.json")
									# drive = GoogleDrive(gauth)
									##auth complete###
									# areainfobotsheet = drive.CreateFile({'id':'1Prra8o6HXS2R6H1fq_4e1IZh4bB2O8WobA9mCy8V-j4'})
									# areainfobotsheet.FetchMetadata()
									# areainfobotsheet.GetContentFile('area_info.csv', mimetype='text/csv')
									# areafile = open('area_info.csv', 'r', encoding='utf-8')
									# areareader = csv.reader(areafile)
									# class_level = "none"
									# for area_row in areareader:
										# if area_row[0] == area:
											# class_level = area_row[1]
											# class_time_start = area_row[2]
											# class_time_end = area_row[3]
											# class_address = area_row[4]
										# elif area_row[0] != area:
											# send_message(sender_id, "Area not included yet.")
									# class_level_formed = ""
									# if "1" in class_level:
										# class_level_formed =  class_level_formed + "Parent/Child Class"
									# if "2" in class_level:
										# class_level_formed =  class_level_formed + "Beginner Class"
									# if "3" in class_level:
										# class_level_formed =  class_level_formed + "Intermediate Class"
									# if "4" in class_level:
										# class_level_formed =  class_level_formed + "Advanced Class"
									# if "5" in class_level:
										# class_level_formed =  class_level_formed + "General Class"
									#better handle multiple classes at one location
									# full_message_area = '''For area %s:\n

# Class level(s): %s\n
# Time of class(es): %s till %s\n
# Class address(es): %s''' % (area, class_level_formed, class_time_start, class_time_end, class_address)
									# if class_level == "none":
										#Temporary fix, replace with update.
										# send_message(sender_id, "Either no classes are taught at this location or there is a gap in our knowledge. Please contact boyd.christiansen on LINE.")
									# else:
										# send_message(sender_id, full_message_area)
								# elif only_one == 2:
									# send_message(sender_id, 'It looks you have made a mistake while trying to get info about a area and accidentally entered more than one area. Please enter only one area at a time.')
								# else:
									# send_message(sender_id, 'You were never supposed to see this message. A serious error has occured. Please contact boyd.christiansen on LINE immediately.')
							# ignore_else = 1
							
						if 'sheet' in message_text:
							area = "none"
							only_one, area = which_area(message_text)
							if only_one == 0:
								send_message(sender_id, 'No valid area name detected, please type "Area List" for a list of areas you can unsubscribe from.')
								ignore_else = 1
							elif only_one == 1:
								#creates a google sheet with referrals for a specific area.
								#Authorize
								gauth = GoogleAuth()
								# # Try to load saved client credentials
								gauth.LoadCredentialsFile("credentials.json")
								if gauth.credentials is None:
									# # Authenticate if they're not there   0auth2
									gauth.LocalWebserverAuth()
								elif gauth.access_token_expired:
									# # Refresh them if expired
									gauth.Refresh()
								else:
									# #Initialize the saved creds
									gauth.Authorize()
								# # Save the current credentials to a file
								gauth.SaveCredentialsFile("credentials.json")
								drive = GoogleDrive(gauth)
								###auth complete###
								####################Access referral database, get the appropriate referrals for the users area and put them in list arearefs
								send_message(sender_id, "Alrighty, google sheet for %s coming up. It might take a few seconds." % (area))
								file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
								for file in file_list:
									if file['title'] == area + ' English Class Referrals':
										file.Delete()
								refdatabase = drive.CreateFile({'id':'1Q2xMx_TJwndYrEB2cyX4MK3dchMkvuUPPD6xuU4Osfw'})
								refdatabase.GetContentFile('refdatabase.csv', mimetype='text/csv')
								referrals = open('refdatabase.csv', "r", newline='', encoding='utf-8')
								rdb = csv.reader(referrals)
								arearefs = []
								for referral in rdb:
									if referral[4] == area:
										arearefs.append(referral)
								#####################Create a new sheet for that area, populate it using the list arearefs.
								nareasheet = open('areasheet.csv', "w", newline='', encoding='utf-8')
								writenewrefs = csv.writer(nareasheet)
								for locref in arearefs:
									writenewrefs.writerow(locref)
								referrals.close()
								nareasheet.close()
								areasheet = drive.CreateFile({'title':area + ' English Class Referrals',
															  "mimeType": "text/csv"})
								areasheet.SetContentFile('areasheet.csv')
								areasheet.Upload({'convert': True})
								permission = areasheet.InsertPermission({'type': 'anyone',
																		 'value': 'anyone',
																		 'role': 'writer'})
								send_message(sender_id, "Here you go!\n" + areasheet['alternateLink'])
								ignore_else = 1
							else:
								send_message(sender_id, 'You were never supposed to see this message. A serious error has occured. Please contact boyd.christiansen on LINE immediately.')
								ignore_else = 1
						if 'unsubscribe' in message_text:
							area = "none"
							only_one, area = which_area(message_text)
							if only_one == 0:
								send_message(sender_id, 'No valid area name detected, please type "Area List" for a list of areas you can unsubscribe from.')
							elif only_one == 1:
								gauth = GoogleAuth()
								# # Try to load saved client credentials
								gauth.LoadCredentialsFile("credentials.json")
								if gauth.credentials is None:
									# # Authenticate if they're not there   0auth2
									gauth.LocalWebserverAuth()
								elif gauth.access_token_expired:
									# # Refresh them if expired
									gauth.Refresh()
								else:
									# #Initialize the saved creds
									gauth.Authorize()
								# # Save the current credentials to a file
								gauth.SaveCredentialsFile("credentials.json")
								drive = GoogleDrive(gauth)
								###auth complete###
								eulonbotsheet = drive.CreateFile({'id':'15nNIEKubHxVFnVkxk_mkFRBPmmuHHHMp_E-rpU9OrAQ'})
								eulonbotsheet.FetchMetadata()
								eulonbotsheet.GetContentFile('DEUL.csv', mimetype='text/csv')
								eulfile = open('DEUL.csv', 'r', encoding='utf-8')
								csvreadthispls = csv.reader(eulfile)
								eullist = []
								for eul in csvreadthispls:
									if eul[0] == area and eul[1] == sender_id:
										eul[1] = 'unsubscribed'
									eullist.append(eul)
								eulfile.close()
								eulfile = open('DEUL.csv', 'w', encoding='utf-8')
								roworg = 0
								for weul in eullist:
									for info in weul:
										if roworg % 2 == 0:
											eulfile.write(info + ',')
											roworg = roworg + 1
										elif roworg % 2 != 0:
											eulfile.write(info + '\n')
											roworg = roworg + 1
										else:
											print('rewrite error')
								eulfile.close()
								eulonbotsheet.SetContentFile('DEUL.csv')
								eulonbotsheet.Upload()
								send_message(sender_id, 'Thanks for all you do! You will no longer receive referrals for %s. Have a nice day.' % (area))
							elif only_one == 2:
								send_message(sender_id, 'It looks you have made a mistake while trying to unsubscribe and accidentally entered more than one area. Please enter only one area at a time.')
							else:
								send_message(sender_id, 'You were never supposed to see this message. A serious error has occured. Please contact boyd.christiansen on LINE immediately.')
							ignore_else = 1
						if 'help' in message_text:
							send_message(sender_id, '''Welcome to the help message! Here are the commands you can use:
In order to register to recieve referrals for an area- type: "register(insert transfer password here)(insert your area name here)".
---------
To display the help message- type "help" (you did it!).
---------
Display a list of all the available areas- type "area list".
---------
Unsubscribe your facebook account from recieving referrals from an area- type "unsubscribe(insert area name here)".
---------
Request a google sheet with all of your areas english referrals to date: type "sheet(insert area name here)".
---------
If you have any questions or concerns please contact boyd.christiansen on LINE.''')
							#send_message(sender_id, '''Welcome to the help message!
	#To register  yourself as an English Unit Leader, please send the word "register", the password for this transfer, and your area name in a message to this bot. After you send the message you will receive referrals for the area you registered for. To get a list of areas you can register for please send 'area list'.
	#''')
							ignore_else = 1
						
						#check for and send an area list message
						if 'area list' in message_text:
							send_message(sender_id, '''Here is a list of areas that you can subscribe to receive referrals from. If your English class is not listed here that means it is not yet on the website. If this is the case please message boyd.christiansen on LINE. Areas can be entered in characters or pinyin.

淡水/Danshui
汐止/Xizhi
北投/Beitou
士林/Shulin
內湖/Neihu
松山/Songshan
台北市中心(信義、大安、萬華、大同、中正、中山)/Central Taipei(Xinyi, Daan, Wanhua, Datong, Zhongzheng, Zhongshan)
三重、蘆洲/Sanchong,Luzhou
新莊/Xinzhuang
土城、樹林/Tucheng,Shulin
板橋/Kanban
中和、永和/Zhonghe,Yonghe
木柵/Mujia
新店/Xindian
安坑/Ankang
三峽/Sanxia
林口/Linkou
北桃園/North Taoyuan
南桃園/South Taoyuan
龜山 - 陸光新城/Guishan-Luguang
中壢/Zhongli
八德/Bade
龍潭/Longtan
竹北/Zhubei
竹東/Zhudong
新竹/Xinzhu
竹南/Zhunan
頭份/Toufen
苗栗/Miaoli
宜蘭/Yilan
花蓮/Hualian
鳳林/Fenglin
台東/Taidong
玉里/Yuli''')
							ignore_else = 1
						
						#check for a register message
						if 'register' in message_text:
							#check to see if the password for that transfer is included in the message
							if '0120' in message_text:
								send_message(sender_id, "Registration attempt registered. Correct password entered.")
								
								only_one, area = which_area(message_text)
								
								#PROCESS IF THEIR REGISTRATION MESSAGE WITH PROPPER PASSWORD HAD AN ERROR AND REACT ACCORDINGLY
								if only_one == 0:
									send_message(sender_id, 'No valid area name deteced, please type "Area List" for a list of areas you can register for.')
								elif only_one == 1:
									#TODO: Fix all of this and check to see if the area already had an ID attached to it. Throw error if it does.
									gauth = GoogleAuth()
									# # Try to load saved client credentials
									gauth.LoadCredentialsFile("credentials.json")
									if gauth.credentials is None:
										# # Authenticate if they're not there   0auth2
										gauth.LocalWebserverAuth()
									elif gauth.access_token_expired:
										# # Refresh them if expired
										gauth.Refresh()
									else:
										# #Initialize the saved creds
										gauth.Authorize()
									# # Save the current credentials to a file
									gauth.SaveCredentialsFile("credentials.json")
									drive = GoogleDrive(gauth)
									#---------------------------------------------------------------------------------------------
									# #drive template file  id '16VTx_WY-pWPhpK1lJWxu5t7LjISniE86'
									# #Download csv from drive, handle inside of server,
									keysheet = drive.CreateFile({'id':'15nNIEKubHxVFnVkxk_mkFRBPmmuHHHMp_E-rpU9OrAQ'})
									keysheet.FetchMetadata()
									keysheet.GetContentFile('DEUL.csv', mimetype='text/csv')
									checkifreg = open('DEUL.csv', 'r', encoding='utf-8')
									readit = csv.reader(checkifreg)
									pass_flag = False
									for reul in readit:
										if reul[0] == area and reul[1] != "unsubscribed":
											send_message(sender_id, "Sorry, this area has already been subscribed to.")
											write = False
											pass_flag = True
										elif pass_flag == False:
											write = True
									checkifreg.close()
									if write == True:
										addneweul = open('DEUL.csv', 'a', encoding='utf-8')
										addneweul.write('''
%s,%s''' % (area, sender_id))
										addneweul.close()
										send_message(sender_id, 'Thank you. You have been registered as the English Unit Leader for %s. Have a good transfer and baptize thousands.' %  (area))
									keysheet.SetContentFile('DEUL.csv')
									keysheet.Upload()
								elif only_one == 2:
									send_message(sender_id, 'It looks you have made a mistake while trying to register and have accidentally entered more than one class. Please try again.')
								else:
									send_message(sender_id, 'You were never supposed to see this message. A serious error has occured. Please contact boyd.christiansen on LINE immediately.')
							else:
								send_message(sender_id, "Incorrect password for this transfer please try again.")
						elif ignore_else == 0:
							send_message(sender_id, 'Non command form message detected. Please use one of the keywords to properly tell the bot what to do. Type "Help" for more information on how to use this bot.')
						else:
							pass
							
					#Other data that I can subscribe to using the developer console 
					if messaging_event.get("delivery"):  # delivery confirmation
						pass

					if messaging_event.get("optin"):  # optin confirmation
						pass

					if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
						pass

	return "ok", 200

#Maybe just make this a mode on / route in the future? idk
@app.route('/clear', methods=['POST'])
def clean_dumb_FB_crap_because_we_made_bugs():
	return "ok", 200
	
#JSON template for sending messages back via requests
#TODO: Add subscription service message tagging
	#See breaking change notice for Facebook Messenger Platform V2.2 https://developers.facebook.com/docs/messenger-platform/send-messages/
def send_message(recipient_id, message_text):
	if recipient_id == "unsubscribed":
		pass
	else:
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

def which_area(message_text):
	only_one = 0
	area = 'none'
	danshui = ['淡水','danshui','dan shui']
	xizhi = ['汐止','xizhi','xi zhi']
	beitou = ['北投','beitou','bei tou']
	shulin = ['士林','shulin','shu lin']
	neihu = ['內湖','neihu','nei hu']
	songshan = ['松山','songshan','song shan']
	taipeicentral = ['台北市中心','taipei central','tai pei central']
	sanchongluzhou = ['三重、蘆洲','sanchong','san chong','lu zhou','luzhou']
	xinzhuang = ['新莊','xinzhuang','xin zhuang']
	tuchengshulin = ['土城、樹林','tucheng','tu cheng','shulin','shu lin']
	banqiao = ['板橋','banqiao','ban qiao']
	zhongheyonghe = ['中和、永和','zhonghe','zhong he','yonghe','yong he']
	mujia = ['木柵','mujia','mu jia']
	xindian = ['新店','xindian','xin dian']
	ankang = ['安坑','ankang','an kang']
	sanxia = ['三峽','sanxia','san xia']
	linkou = ['林口','linkou','lin kou']
	ntaoyuan = ['北桃園','north taoyuan','north tao yuan','bei taoyuan','bei tao yuan','beitaoyuan']
	staoyuan = ['南桃園','south taoyuan','south tao yuan','nan taoyuan','nan tao yuan','nantaoyuan']
	guishan = ['龜山 - 陸光新城','guishan','gui shan']
	zhongli = ['中壢','zhongli','zhong li']
	bade = ['八德','bade','ba de']
	longtan = ['龍潭','longtan','long tan']
	zhubei = ['竹北','zhubei','zhu bei']
	zhudong = ['竹東','zhudong','zhu dong']
	xinzhu = ['新竹','xinzhu','xin zhu']
	zhunan = ['竹南','zhunan','zhu nan']
	toufen = ['頭份','toufen','tou fen']
	miaoli = ['苗栗','miaoli','miao li']
	yilan = ['宜蘭','yilan','yi lan']
	hualian = ['花蓮','hualian','hua lian']
	fenglin = ['鳳林','fenglin','feng lin']
	taidong = ['台東','taidong','tai dong']
	yuli = ['玉里','yuli','yu li']
	#TODO: Reduce these two lists so that we parse the area name used by the program off of the first item in the above list.
	arealist = [
	[danshui,'淡水'],
	[xizhi,'汐止'],
	[beitou,'北投'],
	[shulin,'士林'],
	[neihu,'內湖'],
	[songshan,'松山'],
	[taipeicentral,'台北市中心(信義、大安、萬華、大同、中正、中山)'],
	[sanchongluzhou,'三重、蘆洲'],
	[xinzhuang,'新莊'],
	[tuchengshulin,'土城、樹林'],
	[banqiao,'板橋'],
	[zhongheyonghe,'中和、永和'],
	[mujia,'木柵'],
	[xindian,'新店'],
	[ankang,'安坑'],
	[sanxia,'三峽'],
	[linkou,'林口'],
	[ntaoyuan,'北桃園'],
	[staoyuan,'南桃園'],
	[guishan,'龜山'],
	[zhongli,'中壢'],
	[bade,'八德'],
	[longtan,'龍潭'],
	[zhubei,'竹北'],
	[zhudong,'竹東'],
	[xinzhu,'新竹'],
	[zhunan,'竹南'],
	[toufen,'頭份'],
	[miaoli,'苗栗'],
	[yilan,'宜蘭'],
	[hualian,'花蓮'],
	[fenglin,'鳳林'],
	[taidong,'台東'],
	[yuli,'玉里']
	]
	
	for group in arealist:
		for areaname in group[0]:
			if areaname in message_text:
				start_parse_state = only_one
				area = group[1]
				only_one = 1
			elif areaname in message_text and start_parse_state != 0:
				only_one = 2
	return (only_one, area)