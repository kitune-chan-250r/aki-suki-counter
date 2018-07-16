# coding:utf-8

import os
import sys
import httplib2
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import requests
import json
import time


start_time = time.time()
channelid = "UCt9qik4Z-_J-rj3bKKQCeHg" #アキくんチャンネル　UCt9qik4Z-_J-rj3bKKQCeHg
credentials_path = "youtubeapiplac.py-oauth2.json"
url = "https://www.googleapis.com/youtube/v3/search?part=snippet" 
url += "&channelId=" + channelid + "&type=video&eventType=live"

count_word = {
	"アキくんすき" : 0,
	"アキくん好き" : 0,
	"アキくんスコポンジ" : 0,
	"アキくんすし" : 0,
	"アキくん寿司" : 0
}

def get_comment(chatids):
	return chat_dic[chatids]

def live_status():
	store = Storage(credentials_path)
	credentials = store.get()
	http = credentials.authorize(httplib2.Http())
	res, data = http.request(url)
	jtemp = json.loads(data)
	try:
		jtemp["items"][0]["snippet"]["liveBroadcastContent"]
	except IndexError:
		return False
	else:
		return True

def print_live_not_active():
	elapsed_time = time.time() - start_time
	str_live_not_active = "ライブがアクティブではありません({0})".format(elapsed_time)
	sys.stdout.write("\r\033[K" + str_live_not_active)
	sys.stdout.flush()
	time.sleep(1)

def aki_suki_counter(comment):
	for wordbox in count_word:
		if comment.find(wordbox) >= 0:
			count_word[wordbox] += 1
			print("\n###### +1 counted ######\n")

def print_result():
	print("結果")
	for temp in count_word.keys():
		print("{0} = {1}".format(temp,count_word[temp]))
	suki_num = count_word["アキくんすき"] + count_word["アキくん好き"]
	print("合計アキくんすき = {0}".format(suki_num))
	
#video ID取得
while True:
	if not live_status:
		break

	store = Storage(credentials_path)
	credentials = store.get()

	http = credentials.authorize(httplib2.Http())
	res, data = http.request(url)
	jtemp = json.loads(data)

	try:
		videoid = jtemp["items"][0]["id"]["videoId"]
	except (IndexError, KeyError):
		print_live_not_active()
		continue
	else:
		print("コメント取得を開始します")
		break

#チャットID取得
get_chatid_url = "https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id="
get_chatid_url += videoid

chatid_tmp = http.request(get_chatid_url)
jchatid_tmp = json.loads(chatid_tmp[1])

chatid = jchatid_tmp["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
#コメント内でカウントする言葉
commentlist = []

#チャットIDを元にチャットデータを取得
get_chat_url = "https://www.googleapis.com/youtube/v3/liveChat/"\
				"messages?part=snippet,authorDetails&liveChatId=" 
get_chat_url += chatid

chatid_list = []
chatid_list_set_old = set([])
chat_dic = {}

while live_status():
	commentlist.clear()
	jchat_data = http.request(get_chat_url)
	chat_data = json.loads(jchat_data[1])
	
	try:
		discri = chat_data["items"]
	except IndexError:
		break
	else: 
		for chatbox in chat_data["items"]:
			try:
				temp = chatbox["snippet"]["textMessageDetails"]["messageText"]
			except KeyError:
				print("###### keyerrorが発生 ######")
				continue
			chatid_list.append(chatbox["id"])
			chat_dic[chatbox["id"]] = temp

		chatid_list_set = set(chatid_list)
		chatid_list.clear()
		available_chatid = chatid_list_set - chatid_list_set_old
		ava_c_id = list(available_chatid)
		#アキくんすき判定
		for idbox in ava_c_id:
			sys.stdout.write("\r\033[K" + get_comment(idbox) + "\n>>now count=" \
							+ str(count_word["アキくんすき"] + count_word["アキくん好き"]))
			sys.stdout.flush()
			aki_suki_counter(idbox)
		chatid_list_set_old = chatid_list_set	
		time.sleep(3.5)
		
print_result()

"""
アキくんすし(寿司)
アキくんスコポンジ
アキくんスコティッシュフォールド
							の追加
"""




