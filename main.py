import firebase_admin

from firebase_admin import credentials, firestore
import time

cred = credentials.Certificate("securityAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def profile_names(uid):
    names_ref = db.collection(u'profiles').get()
    for i in names_ref:
        names = i.get('name')
        if uid == i.id:
            return names


def on_snapshot(doc_snapshot, changes, read_time):
    print(
        '_____________________________________________________________________________________________________________')

    for doc in doc_snapshot:
        messages = doc.to_dict()
        sender = profile_names(messages.get('from'))
        recipient = profile_names(messages.get('to'))
        time_of_reception = messages.get('time')
        text = messages.get('body')

        print(f"sender:     {sender}")
        print(f"recipient:  {recipient}")
        print(f"time:       {time_of_reception}")
        print(f"text:       {text}")
        print(
            '_____________________________________________________________________________________________________________')


# Creates a reference to the messages collection
doc_ref = db.collection('messages').order_by('time', direction=firestore.Query.DESCENDING).limit(10)
doc_watch = doc_ref.on_snapshot(on_snapshot)

# Keep the app running
while True:
    time.sleep(0.1)
