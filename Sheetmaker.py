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

# #def sheetmaker(area):
# ####################Access referral database, get the appropriate referrals for the users area and put them in list arearefs
# refdatabase = drive.CreateFile({'id':'1Q2xMx_TJwndYrEB2cyX4MK3dchMkvuUPPD6xuU4Osfw'})
# refdatabase.GetContentFile('refdatabase.csv', mimetype='text/csv')
# referrals = open('refdatabase.csv', "r", encoding='utf-8')
# referrals.read()
# for x in referrals:
	# print(x)
# # #####################Create a new sheet for that area, populate it using the list arearefs.
# # nareasheet = open('areasheet.csv', "w", encoding='utf-8')
# # nareasheet.write()
# # areasheet = drive.CreateFile({'title':area + ' English Class Referrals',
							# # "mimeType": "text/csv"})
# # areasheet.SetContentFile('areasheet.csv')
# # areasheet.Upload(param={'convert': True})
# referrals.close()
# #sheetmaker('中和、永和')

def sheetmaker(area):
####################Access referral database, get the appropriate referrals for the users area and put them in list arearefs
	file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
	for drivefile in file_list:
			if area + ' English Class Referrals' != drivefile['title']:
				refdatabase = drive.CreateFile({'id':'1Q2xMx_TJwndYrEB2cyX4MK3dchMkvuUPPD6xuU4Osfw'})
				refdatabase.GetContentFile('refdatabase.csv', mimetype='text/csv')
				referrals = open('refdatabase.csv', "r", encoding='utf-8')
				rdb = csv.reader(referrals)
				arearefs = []
				for referral in rdb:
					# if referral['Select-5'] == area:
					if referral[4] == area:
						arearefs.append(referral)
				#####################Create a new sheet for that area, populate it using the list arearefs.
				nareasheet = open('areasheet.csv', "w", encoding='utf-8')
				#fieldnames = ['Submitted On','Text-6','Text-8','Radio-2','Select-5','LINE ID','Text-9','Radio-3','Textarea-10','Radio-4','Source']
				#writenewrefs = csv.DictWriter(nareasheet, fieldnames=fieldnames)
				writenewrefs = csv.writer(nareasheet)
				for locref in arearefs:
					writenewrefs.writerow(locref)
				referrals.close()
				nareasheet.close()
				areasheet = drive.CreateFile({'title':area + ' English Class Referrals',
											"mimeType": "text/csv"})
				areasheet.SetContentFile('areasheet.csv')
				areasheet.Upload(param={'convert': True})
			elif area + ' English Class Referrals' == drivefile['title']:
				pass
			else:
				print("ERROR")
sheetmaker('中和、永和')
# 台東/Taidong
# 竹北/Zhubei
# 桃園/Taoyuan
# 鳳林/Fenglin
# 新竹/Xinzhu
# 新店/Xindian
# 桃二/Taoer
# 士林/Shulin
# 苗栗/Miaoli
# 看板/Kanban
# 安坑/Ankang
# 淡水/Danshui
# 木柵/Muzha
# 宜蘭/Yilan
# 台北市中心(信義、大安、萬華、大同、中正、中山)/Taibei City (Xinyi, Daan, Wanhua, Datong, Zhongzheng, Zhongshan)
# 頭份/Toufen
# 林口/Linkou
# 新莊/Xinzhuang
# 北投/Beitou
# 龍潭/Longtan
# 松山/Songshan
# 三峽/Sanxia
# 內湖/Neihu
# 八德/Bade
# 土城、樹林/Tucheng,Shilin
# 竹東/Zhudong
# 板橋/Banqiao
# 龜山-陸光新城/Guishan-Luguang
# 花蓮/Hualian
# 汐止/Xizhi
# 竹南/Zhunan
# 中壢/Zhongli
# 三重、蘆洲/Sanchong,Luzhou
# 基隆/Jilong
# 羅東/Luodong
# 中和、永和/Zhonghe,Yonghe
	
	