import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_all_collection(collection):
    docs = db.collection(collection).stream()
    data = []
    for doc in docs:
        item = doc.to_dict()
        item['id'] = doc.id
        data.append(item)
    return data

