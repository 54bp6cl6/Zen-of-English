import os
import sys
import logging
import json
import flex_template as flex
import dateQ, houseQ
import random
from linebot.models import (TextSendMessage, TemplateSendMessage)
from linebot import (
	LineBotApi, WebhookHandler
)
import db_function as db

line_bot_api = LineBotApi(os.environ.get('TOKEN', 'Specified environment variable is not set.'))
handler = WebhookHandler(os.environ.get('SECRET', 'Specified environment variable is not set.'))

themes = {
	'date': dateQ.DateQ, 'house': houseQ.HouseQ,
}

def next_question(user_id):
	lock = db.get_lock(user_id)
	if lock != '':
		if lock in themes:
			selected = themes[lock](lock)
			selected.answer_break(user_id)
		db.free_lock(user_id)

keywords = {
	'下一題': next_question
}

def callback(request):
	try:
		# 取得事件JSON
		body = request.get_data(as_text=True)
		event = json.loads(body)['events'][0]
		# 設置常用變數
		replyToken = event['replyToken']
		try:
			# Message Event
			if event['type'] == 'message':
				# 設置常用變數
				user_id = event['source']['userId']
				text = event['message']['text']
				# 檢查關鍵字
				if text in keywords:
					keywords[text](user_id)
				# 檢查主題鎖定
				lock = db.get_lock(user_id)
				# 沒有鎖定
				if lock == '':
					if text in themes:
						selected = themes[text](text)
					else:
						selected = random.choice([*themes])
						selected = themes[selected](selected)
				# 有鎖定
				else:
					if lock in themes:
						selected = themes[lock](lock)
					else:
						db.free_lock(user_id)
						selected = random.choice([*themes])
						selected = themes[selected](selected)
				# 執行主題物件並傳送訊息
				line_bot_api.reply_message(replyToken, selected.handle_message(event))
				# 執行主題收尾工作
				selected.final_process()
			#Postback Event
			elif event['type'] == 'postback':
				data = json.loads(event['postback']['data'])
				if data['theme'] in themes:
					selected = themes[data['theme']](data['theme'])
					line_bot_api.reply_message(replyToken, selected.handle_postback(event))
					selected.final_process()
		# 在Line上面Debug
		except Exception as e:
			line_bot_api.reply_message(replyToken, TextSendMessage(text="main.py:{0}".format(e)))
	# 在主控台Debug
	except:
		logging.error(sys.exc_info())
		return 'ERROR'
	return 'OK'
