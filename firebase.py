import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("ecocampus-7e7c8-firebase-adminsdk-fbsvc-61b807e0fa.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def save_record(data, inputs):
    record = {
        **inputs,
        **data,
        "timestamp": firestore.SERVER_TIMESTAMP
    }

    db.collection("campus_records").add(record)


def get_history():
    records = db.collection("campus_records").stream()

    history = []

    for record in records:
        history.append(record.to_dict())

    return history