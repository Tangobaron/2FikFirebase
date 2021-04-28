import firebase_admin
from watchpoints import watch
from firebase_admin import credentials, firestore
from td_client import TDClient
from twofik_localisation import Twofik
import time
import socket
import sys
import threading

cred = credentials.Certificate("venv/securityAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
sVar = None

#server related variable
class serverVar():
    testing = False
    TD_CLI = TDClient('localhost', 5786)
    isAlive = False
    twoFik = Twofik(cred,db,'uTS21weWNkbggwHu16ScM1Nqart1')
    doc_watch = None
    terminateThread = False
    lastName = None
    initMessage = False
    callbackDone = threading.Event()


def main():
    global sVar
    if sVar is None:
        sVar = serverVar()
    if sVar.isAlive is False:
        if sVar.testing: print("Initialise server")
        # Creates a reference to the messages collection
        #doc_ref = db.collection('messages').order_by('time', direction=firestore.Query.DESCENDING).limit(5)
        sVar.isAlive = init()
    if sVar.lastName != sVar.twoFik.ChatWith:
        if sVar.testing: print("----------------------| updating message query")
        queryChat()
        sVar.lastName = sVar.twoFik.ChatWith

# Follow 2fik location in real time

def init():
    global sVar
    #twoFikID = twofik_location(True)
    # start listener on message collection
    #collection_ref = db.collection('messages')
    #fik_ref = collection_ref.where(u'from', u'==',  twoFikID).limit(10) 
    #serverVar.doc_watch = fik_ref.on_snapshot(on_snapshot)
    # create twoFik status object and start listening on it<s in app location
    sVar.twoFik.Follow2fik()
    #watch(twoFik.Name,callback=ChangeQuery)
    #watch(sVar.twoFik.Name,callback=ChangeQuery)
    return True

def queryChat():
    global sVar
    collection_ref = db.collection('messages')
    if sVar.testing: print(f'twofik id: {sVar.twoFik.Name}')
    fik_ref = collection_ref.where(u'from', u'==',  sVar.twoFik.Name).limit(30)
    if sVar.testing: print(f'Twofik ID: {sVar.twoFik.Name}')
    profile_ref = fik_ref.where(u'to', u'==', sVar.twoFik.ChatWith)
    sVar.doc_watch = profile_ref.on_snapshot(on_snapshot)
    if sVar.doc_watch is not None:
        if sVar.testing: print("remove listener after the callback trigger")
        sVar.terminateThread = True
        sVar.callbackDone.wait(timeout=30)
        sVar.doc_watch.unsubscribe()
        sVar.initMessage = False
    try:
        sVar.doc_watch = profile_ref.on_snapshot(on_snapshot)
    except:
        if sVar.testing: print('cannot create snapshot object')
    if sVar.testing: print('finished with queryChat')

def ChangeQuery(frame, elem, exec_info):
    if sVar.testing: print("change query but fonction is not finish")
    queryChat()

# Extract the names of the 2Fik profiles according to their UIDs
def twofik_profile_names():
    names_ref = db.collection(u'profiles').get()
    for i in names_ref:
        if i.get('state') == '2fik':
            names = i.get('name')
            uid = i.id
            if sVar.testing: print(f'{uid} ->  {names}')

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
    if sVar.testing: print('______________________________________________________________________________')
    if sVar.testing: print(f'profile used : {profile_selected}')
    if sVar.testing: print(body_state)
    if sVar.testing: print(panel_state)
    if sVar.testing: print('______________________________________________________________________________')
    if getID == True:
        return profile_selected
    else:
        return get_real_name(profile_selected)


# Receives each messages depending on which persona is 2Fik incarning
def on_snapshot(doc_snapshot, changes, read_time):
    if sVar.testing: print('_____________________________________________________________________________________________________________')
    if sVar.initMessage is True:
        for change in changes:
            if sVar.testing: print(f'changeType: {change.type.name}')
            if change.type.name == 'ADDED':
                doc = change.document
                #doc = change.after()
                messages = doc.to_dict()
                if sVar.testing: print('__________________________________________________\\\\_______________________________________________________')
                if sVar.testing: print(f'messages: {messages}')
                if sVar.testing: print('__________________________________________________\\\\\______________________________________________________')
                sender = get_real_name(messages.get('from'))
                recipientID = messages.get('to')
                recipient = get_real_name(recipientID)
                #print(f'recipient: {recipient}')
                time_of_reception = messages.get('time')
                text = messages.get('body')
                nameList = ["sender", "recipient", "recipientID", "time", "text"]
                dataList = [str(sender), str(recipient), str(recipientID), str(time_of_reception), str(text)]
                sVar.TD_CLI.AddToBuffer(nameList, dataList)
        sVar.TD_CLI.SendMessage()
    else:
        if sVar.testing: print('entering else')
        if sVar.testing: print(f'doc_snapshot: {doc_snapshot}' )
        for doc in doc_snapshot:
            messages = doc.to_dict()
            #print(f'messages: {messages}')
            sender = get_real_name(messages.get('from'))
            recipientID = messages.get('to')
            recipient = get_real_name(recipientID)
            #print(f'recipient: {recipient}')
            time_of_reception = messages.get('time')
            text = messages.get('body')
            nameList = ["sender", "recipient", "recipientID", "time", "text"]
            dataList = [str(sender), str(recipient), str(recipientID), str(time_of_reception), str(text)]
            sVar.TD_CLI.AddToBuffer(nameList, dataList)
            if sVar.testing: print(f"sender:     {sender}")
            if sVar.testing: print(f"recipient:  {recipient}")
            if sVar.testing: print(f"time:       {time_of_reception}")
            if sVar.testing: print(f"text:       {text}")
            if sVar.testing: print('_____________________________________________________________________________________________________________')
        sVar.initMessage = True
        sVar.TD_CLI.SendMessage()
    sVar.callbackDone.set()
    if sVar.testing: print("finished query")


while True:
    try:
        time.sleep(0.1)
        main()
    except KeyboardInterrupt:
        if sVar.testing: print('manual interupt')
        sys.exit()
#if __name__=="__main__":
#    try:
#        main()
#    except KeyboardInterrupt:
#        print('interrupted')
#        pass
