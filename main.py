import firebase_admin
from watchpoints import watch
from firebase_admin import credentials, firestore
from td_client import TDClient
from twofik_localisation import Twofik
from snapshot_class import Snapshot as Listener
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
    queryLimit = 30
    CLI_from = TDClient('localhost', 5786)
    CLI_to = TDClient('localhost', 5788)
    isAlive = False
    twoFik = Twofik(cred,db,'uTS21weWNkbggwHu16ScM1Nqart1', DEBUG=False)
    doc_watch = None
    lastName = None
    initMessage = False
    FromListener = Listener(db, CLI_from, ACTION="Sent", DEBUG=False)
    toListener = Listener(db, CLI_to, ACTION="Received", DEBUG=False)
    #callbackDone = threading.Event()


def main():
    global sVar
    if sVar is None:
        sVar = serverVar()
    if sVar.isAlive is False:
        if sVar.testing: print("Initialise server")
        # Creates a reference to the messages collection
        sVar.isAlive = init()
    if sVar.lastName != sVar.twoFik.ChatWith:
        if sVar.testing: print("----------------------| updating message query")
        queryChat()
        sVar.lastName = sVar.twoFik.ChatWith

# Follow 2fik location in real time

def init():
    global sVar
    sVar.twoFik.Follow2fik()
    return True

def queryChat():
    global sVar

    collection_ref = db.collection('messages')
    if sVar.testing: print(f'twofik id: {sVar.twoFik.Name}')

    fik_ref = collection_ref.where(u'from', u'==',  sVar.twoFik.Name).limit(sVar.queryLimit).where(u'to', u'==', sVar.twoFik.ChatWith)
    recipient_ref = collection_ref.where(u'to', u'==', sVar.twoFik.Name).limit(sVar.queryLimit).where(u'from', u'==',  sVar.twoFik.ChatWith)
    
    sVar.FromListener.SetNewListener(fik_ref)
    sVar.toListener.SetNewListener(recipient_ref)
    
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

while True:
    try:
        time.sleep(0.1)
        main()
    except KeyboardInterrupt:
        if sVar.testing: print('manual interupt')
        sys.exit()

