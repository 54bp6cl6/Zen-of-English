import firebase_admin
from firebase_admin import (
	credentials,firestore
)

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {'projectId': 'english-265904'})

db = firestore.client()

def write_test():
	doc_ref = db.collection(u'users').document(u'alovelace')
	doc_ref.set({
		u'first': u'Ada',
		u'last': u'Lovelace',
		u'born': 1815
	})

def read_test():
	doc_ref = db.collection(u'users').document(u'alovelace')
	return doc_ref.get().exists

def get_lock(user_id):
	doc_ref = db.collection(u'users').document(user_id)
	if doc_ref.get().exists:
		try:
			return doc_ref.get().to_dict()['lock']
		except KeyError:
			doc_ref.update({u'lock': u''})
	else:
		doc_ref.set({u'lock': u''})
	return ''

def set_lock(user_id, theme):
	doc_ref = db.collection(u'users').document(user_id)
	if doc_ref.get().exists:
		doc_ref.update({u'lock': theme})
	else:
		doc_ref.set({u'lock': theme})

def free_lock(user_id):
	set_lock(user_id, '')

def set_vars(theme, user_id, data):
	db.collection(theme).document(user_id).set(data)

def update_vars(theme, user_id, data):
	doc_ref = db.collection(theme).document(user_id)
	if doc_ref.get().exists:
		doc_ref.update(data)
	else:
		doc_ref.set(data)

def get_vars(theme, user_id):
	doc_ref = db.collection(theme).document(user_id)
	if doc_ref.get().exists:
		return doc_ref.get().to_dict()
	else:
		return {}