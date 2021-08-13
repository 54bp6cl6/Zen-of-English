import random
import flex_template as flex
import db_function as db
import json

class DateQ():
	def __init__(self, name):
		self.name = name
		self.vocabulary = {
			'一月':'January', '二月':'February',   '三月':'March',
			'四月':'April',   '五月':'May',        '六月':'June',
			'七月':'July',    '八月':'August',     '九月':'September',
			'十月':'October', '十一月':'November', '十二月':'December'
		}
		self.question_types = {'英翻中': self.en_to_ch, '中翻英': self.ch_to_en, '是非題': self.tf_test, '手寫題': self.handwriting }
		self.need_save = False

	def handle_message(self, event):
		try:
			self.user_id = event['source']['userId']
			data = db.get_vars(self.name, self.user_id)
			if 'ans' in data and data['ans'] != '':
				if event['message']['text'].strip().lower() == data['ans'].lower():
					db.free_lock(self.user_id)
					db.update_vars(self.name, self.user_id, {'ans':''})
					return flex.single_button_message('答對了!', '下一題', '#b0d392')
				else:
					return flex.single_button_message('答錯了~再試試吧!', '下一題', '#e2b5b1')

			if 'avalible' in data:
				self.avalible = data['avalible']
			else:
				self.avalible = [*self.vocabulary]

			type_limit = random.choice([*self.question_types])
			return self.question_types[type_limit](type_limit)
			
		except Exception as e:
			return flex.error('date.py(handle_message):{0}'.format(e))
	
	def handle_postback(self, event):
		try:
			data = json.loads(event['postback']['data'])
			if data['situation'] == 'right':  return flex.single_button_message('答對了!', '下一題', '#b0d392')
			elif data['situation'] == 'wrong': return flex.single_button_message('答錯了~再試試吧!', '下一題', '#e2b5b1')
			else: return flex.error('喔喔~這個按鈕失去作用了')
		except Exception as e:
			return flex.error('dateQ.py(handle_postback):{0}'.format(e))

	def final_process(self):
		if self.need_save:
			if len(self.avalible) == 0: self.avalible = [*self.vocabulary]
			self.save_avalible_record()
			self.need_save = False

	def answer_break(self, user_id):
		db.update_vars(self.name, user_id, {'ans': ''})

	def get_avalible_record(self, user_id):
		data = db.get_vars(self.name, user_id)
		if 'avalible' in data:
			self.avalible = data['avalible']
		else:
			self.avalible = [*self.vocabulary]

	def save_avalible_record(self):
		db.update_vars(self.name, self.user_id, {'avalible': self.avalible})

	def select_word(self):
		try:
			ch_ans = random.choice([*self.avalible])
		except:
			self.avalible = [*self.vocabulary]
			ch_ans = random.choice([*self.avalible])
		en_ans = self.vocabulary[ch_ans]
		self.avalible.remove(ch_ans)
		self.need_save = True
		return ch_ans, en_ans

	def en_to_ch(self, type_limit, option_num=3):
		ch_ans, en_ans = self.select_word()
		options = [ch_ans]
		temp = [*self.vocabulary]
		temp.remove(ch_ans)
		for i in range(option_num-1):
			choose = random.choice(temp)
			options.append(choose)
			temp.remove(choose)
		random.shuffle(options)
		return flex.multiple_choice(type_limit, en_ans, options, ch_ans, self.name)

	def ch_to_en(self, type_limit, option_num=3):
		ch_ans, en_ans = self.select_word()
		options = [en_ans]
		temp = [*self.vocabulary.values()]
		temp.remove(en_ans)
		for i in range(option_num-1):
			choose = random.choice(temp)
			options.append(choose)
			temp.remove(choose)
		random.shuffle(options)
		return flex.multiple_choice(type_limit, ch_ans, options, en_ans, self.name)

	def tf_test(self, type_limit):
		ch_ans, en_ans = self.select_word()
		ans = random.choice([True, False])
		key = random.choice([en_ans, ch_ans])
		value = en_ans if key == ch_ans else ch_ans
		if ans:
			return flex.tf_test(type_limit, key, value, ans, self.name)
		else:
			if key == en_ans:
				temp = [*self.vocabulary]
			else:
				temp = [*self.vocabulary.values()]
			temp.remove(value)
			value = random.choice(temp)
			return flex.tf_test(type_limit, key, value, ans, self.name)

	def handwriting(self, type_limit):
		ch_ans, en_ans = self.select_word()
		db.update_vars(self.name, self.user_id, {'ans': en_ans})
		db.set_lock(self.user_id, self.name)
		return flex.handwriting(type_limit, '這個單字的英文是?', ch_ans, en_ans)