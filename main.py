import firebase_admin

from firebase_admin import credentials, firestore
from td_client import TDClient
import time
import socket
import sys

cred = credentials.Certificate("venv/securityAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#server related variable
TD_CLI = TDClient('localhost', 5786) 
isAlive = False
def main():
    global isAlive
    if isAlive is False:
        # Creates a reference to the messages collection
        #doc_ref = db.collection('messages').order_by('time', direction=firestore.Query.DESCENDING).limit(5)
        doc_ref = db.collection('messages').order_by('time', direction=firestore.Query.DESCENDING).limit(5)
        doc_watch = doc_ref.on_snapshot(on_snapshot)
        isAlive = True

# Extract the names of the 2Fik profiles according to their UIDs
def twofik_profile_names():
    names_ref = db.collection(u'profiles').get()
    for i in names_ref:
        if i.get('state') == '2fik':
            names = i.get('name')
            uid = i.id
            print(f'{uid} ->  {names}')


# Gets a single real name from a UID
def get_real_name(uid):
    names_ref = db.collection(u'profiles').get()
    for name in names_ref:
        if uid == name.id:
            return name.get('name')


# Where is 2Fik in the app and which profile is he using
def twofik_location():
    # super user to track (in this case Raph for now)
    identification = 'pX94rzzZRTOfluPkLuRZZKkUmFY2'

    # firebase database reference
    location_ref = db.collection(u'location').document(identification).get()
    dictionary = location_ref.to_dict()

    # get 2Fik's current profile used
    profile_selected = location_ref.get('profile')

    # Which body is 2Fik in
    body = dictionary['body']
    body_state = body.get('state')

    # Which panel is 2Fik on
    panel = dictionary['panel']
    panel_state = panel.get('state')

    return get_real_name(profile_selected)

    print('______________________________________________________________________________')
    print(f'profile used : {profile_selected}')
    print(body_state)
    print(panel_state)
    print('______________________________________________________________________________')


# Receives each messages depending on which persona is 2Fik incarning
def on_snapshot(doc_snapshot, changes, read_time):
    print('_____________________________________________________________________________________________________________')

    for doc in doc_snapshot:
        messages = doc.to_dict()
        print(f'messages: {messages}')
        sender = get_real_name(messages.get('from'))
        recipient = twofik_location()
        print(f'recipient: {recipient}')
        time_of_reception = messages.get('time')
        text = messages.get('body')
        nameList = ["sender", "recipient", "time", "text"]
        dataList = [str(sender), str(recipient), str(time_of_reception), str(text)]
        TD_CLI.SendMessage(nameList, dataList)
        #print(f"sender:     {sender}")
        #print(f"recipient:  {recipient}")
        #print(f"time:       {time_of_reception}")
        #print(f"text:       {text}")
        print('_____________________________________________________________________________________________________________')

# Keep the app running
try:
	main()
except err:
	print(err)

while True:
    time.sleep(0.1)

#if __name__=="__main__":
#    try:
#        main()
#    except KeyboardInterrupt:
#        print('interrupted')
#        pass
