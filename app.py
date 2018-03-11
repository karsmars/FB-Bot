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

				if messaging_event.get("message"):  # someone sent us a message

					sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending the message
					recipient_id = messaging_event["recipient"]["id"]  # our facebook ID number
					message_text = messaging_event["message"]["text"]  # the message's text
					
					#lowercase message text so we don't have to care about capitalization
					message_text = message_text.lower()
					
					#variable that triggers the default response if nobody 
					ignore_else = 0
					
					#TODO: Have users agree to receiving subscription messages.
					
					#check for and send a general help message
					#Unsubscribe
					if 'help' in message_text:
						send_message(sender_id, '''Welcome to the help message!
To register  yourself as an English Unit Leader, please send the word register, the password for this transfer, and your area name in a message to this bot. After you send the message you will receive referrals for the area you registered for. To get a list of areas you can register for please send 'area list'.
''')
						ignore_else = 1
					
					#check for and send an area list message
					if 'area list' in message_text:
						send_message(sender_id, '''Here is a list of areas that you can subscribe to receive referrals from. If your English class is not listed here that means it is not yet on the website. If this is the case please message boyd.christiansen on LINE. Areas can be entered in characters or pinyin.

台東
竹北
桃園
鳳林
新竹
新店
桃二
士林
苗栗
看板
安坑
淡水
木柵
宜蘭
台北市中心(信義、大安、萬華、大同、中正、中山)
頭份
林口
新莊
北投
龍潭
松山
三峽
內湖
八德
土城、樹林
竹東
板橋
龜山-陸光新城
花蓮
汐止
竹南
中壢
三重、蘆洲
基隆
羅東''')
						ignore_else = 1
					
					#check for a register message
					if 'register' in message_text:
						#check to see if the password for that transfer is included in the message
						if '0120' in message_text:
							send_message(sender_id, "Registration attempt registered. Correct password entered.")
							#Only allows for one area per registration message.
							only_one = 0
							#FIGURE OUT WHAT AREA THEY ARE FROM
							#I know this is bad practice, but I can write it really fast. Please replace with a dictionary with error checking puling from a file somewhere.
							#if "yingge" in message_text  or "ying ge" in message_text or "鶯歌" in message_text:
								#if only_one == 0:
									#area = '鶯歌'
									#only_one = 1
								#else:
									#only_one = 2
							
							if "tai dong" in message_text  or "taidong" in message_text or "台東" in message_text:
								if only_one == 0:
									area = '台東'
									only_one = 1
								else:
									only_one = 2
									
							if "zhubei" in message_text  or "zhu bei" in message_text or "竹北" in message_text:
								if only_one == 0:
									area = '竹北'
									only_one = 1
								else:
									only_one = 2
									
							if "taoyuan" in message_text  or "tao yuan" in message_text or "桃園" in message_text:
								if only_one == 0:
									area = '桃園'
									only_one = 1
								else:
									only_one = 2
							
							if "fenglin" in message_text  or "feng lin" in message_text or "鳳林" in message_text:
								if only_one == 0:
									area = '鳳林'
									only_one = 1
								else:
									only_one = 2
									
							if "xinzhu" in message_text  or "xin zhu" in message_text or "新竹" in message_text:
								if only_one == 0:
									area = '新竹'
									only_one = 1
								else:
									only_one = 2
									
							if "xindian" in message_text  or "xin dian" in message_text or "新店" in message_text:
								if only_one == 0:
									area = '新店'
									only_one = 1
								else:
									only_one = 2
									
							if "taoer" in message_text  or "taoer" in message_text or "桃二" in message_text:
								if only_one == 0:
									area = '桃二'
									only_one = 1
								else:
									only_one = 2
							
							if "shilin" in message_text  or "shi lin" in message_text or "士林" in message_text:
								if only_one == 0:
									area = '士林'
									only_one = 1
								else:
									only_one = 2
							
							if "miaoli" in message_text  or "miao li" in message_text or "苗栗" in message_text:
								if only_one == 0:
									area = '苗栗'
									only_one = 1
								else:
									only_one = 2
							
							if "shuanghe" in message_text  or "shuang he" in message_text or "看板" in message_text:
								if only_one == 0:
									area = '看板'
									only_one = 1
								else:
									only_one = 2
							
							if "ankang" in message_text  or "an kang" in message_text or "安坑" in message_text:
								if only_one == 0:
									area = '安坑'
									only_one = 1
								else:
									only_one = 2
							
							if "danshui" in message_text  or "dan shui" in message_text or "淡水" in message_text:
								if only_one == 0:
									area = '淡水'
									only_one = 1
								else:
									only_one = 2
							
							if "muzha" in message_text  or "mu zha" in message_text or "木柵" in message_text:
								if only_one == 0:
									area = '木柵'
									only_one = 1
								else:
									only_one = 2
							
							if "yilan" in message_text  or "yi lan" in message_text or "宜蘭" in message_text:
								if only_one == 0:
									area = '宜蘭'
									only_one = 1
								else:
									only_one = 2
							
							if "central taipei" in message_text  or "central tai pei" in message_text or "central-taipei" in message_text or "台北市中心" in message_text:
								if only_one == 0:
									area = '台北市中心(信義、大安、萬華、大同、中正、中山)'
									only_one = 1
								else:
									only_one = 2
							
							if "toufen" in message_text  or "tou fen" in message_text or "頭份" in message_text:
								if only_one == 0:
									area = '頭份'
									only_one = 1
								else:
									only_one = 2
							
							if "linkou" in message_text  or "lin kou" in message_text or "林口" in message_text:
								if only_one == 0:
									area = '林口'
									only_one = 1
								else:
									only_one = 2
							
							if "xinzhuang" in message_text  or "xin zhuang" in message_text or "新莊" in message_text:
								if only_one == 0:
									area = '新莊'
									only_one = 1
								else:
									only_one = 2
							
							if "beitou" in message_text  or "bei tou" in message_text or "北投" in message_text:
								if only_one == 0:
									area = '北投'
									only_one = 1
								else:
									only_one = 2
							
							if "longtan" in message_text  or "long tan" in message_text or "龍潭" in message_text:
								if only_one == 0:
									area = '龍潭'
									only_one = 1
								else:
									only_one = 2
									
							if "songshan" in message_text  or "song shan" in message_text or "松山" in message_text:
								if only_one == 0:
									area = '松山'
									only_one = 1
								else:
									only_one = 2
									
							if "sanxia" in message_text  or "san xia" in message_text or "三峽" in message_text:
								if only_one == 0:
									area = '三峽'
									only_one = 1
								else:
									only_one = 2
							
							if "neihu" in message_text  or "nei hu" in message_text or "內湖" in message_text:
								if only_one == 0:
									area = '內湖'
									only_one = 1
								else:
									only_one = 2
							
							if "bade" in message_text  or "ba de" in message_text or "八德" in message_text:
								if only_one == 0:
									area = '八德'
									only_one = 1
								else:
									only_one = 2
							
							if "tu cheng" in message_text  or "tucheng" in message_text or "shulin" in message_text or "shu lin" in message_text or "土城" in message_text or "樹林" in message_text:
								if only_one == 0:
									area = '土城、樹林'
									only_one = 1
								else:
									only_one = 2
							
							if "zhu dong" in message_text  or "zhudong" in message_text or "竹東" in message_text:
								if only_one == 0:
									area = '竹東'
									only_one = 1
								else:
									only_one = 2
							
							if "xinpu" in message_text  or "xin pu" in message_text or "板橋" in message_text:
								if only_one == 0:
									area = '板橋'
									only_one = 1
								else:
									only_one = 2
							
							if "luguang" in message_text  or "lu guang" in message_text or "龜山" in message_text:
								if only_one == 0:
									area = '龜山'
									only_one = 1
								else:
									only_one = 2
							
							if "hualian" in message_text  or "hua lian" in message_text or "花蓮" in message_text:
								if only_one == 0:
									area = '花蓮'
									only_one = 1
								else:
									only_one = 2
							
							if "xizhi" in message_text  or "xi zhi" in message_text or "汐止" in message_text:
								if only_one == 0:
									area = '汐止'
									only_one = 1
								else:
									only_one = 2
							
							if "zhu nan" in message_text  or "zhunan" in message_text or "竹南" in message_text:
								if only_one == 0:
									area = '竹南'
									only_one = 1
								else:
									only_one = 2
							
							if "zhongli" in message_text  or "zhong li" in message_text or "中壢" in message_text:
								if only_one == 0:
									area = '中壢'
									only_one = 1
								else:
									only_one = 2
							
							if "san chong" in message_text  or "sanchong" in message_text or "luzhou" in message_text or "lu zhou" in message_text or "三重" in message_text or "蘆洲" in message_text:
								if only_one == 0:
									area = '三重、蘆洲'
									only_one = 1
								else:
									only_one = 2
							
							if "jilong" in message_text  or "ji long" in message_text or "基隆" in message_text:
								if only_one == 0:
									area = '基隆'
									only_one = 1
								else:
									only_one = 2
							
							if "yuli" in message_text  or "yu li" in message_text or "玉里" in message_text:
								if only_one == 0:
									area = '玉里'
									only_one = 1
								else:
									only_one = 2
									
							if "zhonghe" in message_text or "zhong he" in message_text or "中和" in message_text or "yonghe" in message_text or "yong he" in message_text or "永和" in message_text:
								if only_one == 0:
									area = '中和、永和'
									only_one = 1
								else:
									only_one = 2
							#Template for adding future areas
							#if "" in message_text  or "" in message_text or "" in message_text:
								#if only_one == 0:
									#area = ''
									#only_one = 1
								#else:
									#only_one = 2
							#######################
							
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
								
								# #drive template file  id '16VTx_WY-pWPhpK1lJWxu5t7LjISniE86'
								# #Download csv from drive, handle inside of server,
								keysheet = drive.CreateFile({'id':'15nNIEKubHxVFnVkxk_mkFRBPmmuHHHMp_E-rpU9OrAQ'})
								keysheet.FetchMetadata()
								if u'text/csv' not in keysheet.metadata['exportLinks']:
									# #Adds new metadata type that allows csv to read Google Sheets
									keysheet.metadata['exportLinks'][u'text/csv'] = keysheet.metadata['exportLinks'][u'application/pdf'][:-3]+u"csv"
								keysheet.GetContentFile('DEUL.csv', mimetype='text/csv')
								download_mimetype = None
								mimetypes = { 'application/vnd.google-apps.document': 'application/pdf',
									'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
								#read in whole thing as a dictionary
								#or force formatting
								with open('DEUL.csv', 'a', newline='') as csvfile:
									csvfile.write('''
%s,%s''' % (area, sender_id))
									csvfile.close()
									#fieldnames = ['area', 'sender_id']
									#writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
									#writer.writerow({'area': area, 'sender_id': sender_id})
								
								keysheet.SetContentFile('DEUL.csv')
								
								#reupload
								keysheet.Upload()
								
								send_message(sender_id, 'Thank you. You have been registered as the English Unit Leader for %s. Have a good transfer and baptize thousands.' %  (area))
								
								#Fastpatch that has the recorder enter all of the Facebook ID numbers into the csv file that is processed by the local code instead of putting it into a CSV.
								#send_message(sender_id, 'Thank you. You have been registered as the English Unit Leader for %s. Please send the number "%s" to the recorder.' % (area, sender_id))
							elif only_one == 2:
								send_message(sender_id, 'It looks while you have made a mistake while trying to register and have accidentally entered more than one class. Please try again.')
							else:
								send_message(sender_id, 'You were never supposed to see this message. A serious error has occured. Please contact boyd.christiansen on LINE immediately.')
						else:
							send_message(sender_id, "Incorrect password for this transfer please try again.")
					elif ignore_else == 0:
						send_message(sender_id, 'Non-registration message detected, if you are trying to register please use the registration keyword or type "Help" for more information on how to use this bot.')
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
	
#JSON template for sending messages back via requests
#TODO: Add subscription service message tagging
	#See breaking change notice for Facebook Messenger Platform V2.2 https://developers.facebook.com/docs/messenger-platform/send-messages/
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