import firebase_admin

from firebase_admin import credentials, firestore
from td_client import TDClient
from twofik_localisation import Twofik
import time
import socket
import sys

cred = credentials.Certificate("venv/securityAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#server related variable
TD_CLI = TDClient('localhost', 5786)
isAlive = False
initMessage = False
twoFik = Twofik(cred,db,'uTS21weWNkbggwHu16ScM1Nqart1')

def main():
    global isAlive
    if isAlive is False:
        # Creates a reference to the messages collection
        #doc_ref = db.collection('messages').order_by('time', direction=firestore.Query.DESCENDING).limit(5)
        isAlive = init()

# Follow 2fik location in real time

def init():
    global twoFik
    twoFikID = twofik_location(True)
    # start listener on message collection
    collection_ref = db.collection('messages')
    print(f'collection: {collection_ref}')
    fik_ref = collection_ref.where(u'from', u'==',  twoFikID).limit(10) 
    doc_watch = fik_ref.on_snapshot(on_snapshot)
    # create twoFik status object and start listening on it<s in app location
    twoFik.Follow2fik()

    return True

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
def twofik_location(getID = False):
    # super user to track (in this case Raph for now)
    #identification = 'pX94rzzZRTOfluPkLuRZZKkUmFY2'
    identification = 'uTS21weWNkbggwHu16ScM1Nqart1'

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
    print('______________________________________________________________________________')
    print(f'profile used : {profile_selected}')
    print(body_state)
    print(panel_state)
    print('______________________________________________________________________________')
    if getID == True:
        return profile_selected
    else:
        return get_real_name(profile_selected)


# Receives each messages depending on which persona is 2Fik incarning
def on_snapshot(doc_snapshot, changes, read_time):
    global initMessage
    print('_____________________________________________________________________________________________________________')
    
    if initMessage is True:
        for change in changes:
            print(f'changeType: {change.type.name}')
            if change.type.name == 'ADDED':
                #doc = change.document.id
                doc = change.document.to_dict()
                print('_____________________________________________________________________________________________________________')
                print(f'doc: {doc}')
                print('_____________________________________________________________________________________________________________')
                sender = get_real_name(messages.get('from'))
                recipient = get_real_name(messages.get('to'))
                print(f'recipient: {recipient}')
                time_of_reception = messages.get('time')
                text = messages.get('body')
                nameList = ["sender", "recipient", "time", "text"]
                dataList = [str(sender), str(recipient), str(time_of_reception), str(text)]
                TD_CLI.SendMessage(nameList, dataList)

    else:
        for doc in doc_snapshot:
            messages = doc.to_dict()
            print(f'messages: {messages}')
            sender = get_real_name(messages.get('from'))
            recipient = get_real_name(messages.get('to'))
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
        initMessage = True
# Keep the app running
try:
	main()
except KeyboardInterrupt:
        print('interrupted')
        pass
#except Exception as e:
	#print(f'an error occured in main function: {repr(e)}')

while True:
    time.sleep(0.1)

#if __name__=="__main__":
#    try:
#        main()
#    except KeyboardInterrupt:
#        print('interrupted')
#        pass
