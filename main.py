import time
import argparse
import firebase_admin
from firebase_admin import credentials, firestore
from inbox import Inbox as FillInbox
from ranking import Ranking as FillRanking
from td_client import TDClient
from twofik_localisation import Twofik
from snapshot_class import Snapshot as Listener
from inbox import Inbox
from CadavreExquis import CadavreExquis
import time
import socket
import sys
import threading

cred = credentials.Certificate("venv/securityAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
sVar = None
parser = argparse.ArgumentParser(description='2Fik python client. Connect firebase too touchdesigner')
parser.add_argument('id', help='2Fik uid needed to connect to his position and follow is action on the dating app.')
parser.add_argument('-p', '--ports', nargs=5, dest='ports', default=[5780,5784,5786,5788,5792], help='List of port to be use by the app. They are 5 require[inbox,localisation,messageTo2Fik,messageFrom2Fik,HotorNot]')
#parser.add_argument('-d', '--debug', type=int, dest='DEBUG', default=0, help='this variable range from 0 to 3. It determine the level of verbose you\'ll get from the python app. Higher the verbose lower the performance. Let to default for maximum performance')
args = parser.parse_args()


class ServerVar:
    # class containing constant we need through the application
    def __init__(self):
        self.testing = False
        self.isAlive = False
        self.doc_watch = None
        self.lastName = None
        self.twoFikID = None
        self.initMessage = False
        self.queryLimit = 30
        #client that connect to different port of touchdesigner server
        self.CLI_inbox = TDClient('localhost', int(args.ports[0]), DEBUG=False)
        self.CLI_location = TDClient('localhost', int(args.ports[1]), DEBUG=False)
        self.CLI_from = TDClient('localhost', int(args.ports[3]), DEBUG=False)
        self.CLI_to = TDClient('localhost', int(args.ports[2]), DEBUG=False)
        self.CLI_rank = TDClient('localhost', int(args.ports[4]), DEBUG=False)
        #imported class instanciation
        #self.inbox = Inbox(db, self.CLI_inbox, DEBUG=False)
        self.lastMessage = CadavreExquis(db, self.CLI_inbox)
        self.twoFik = Twofik(cred,db,str(args.id), self.CLI_location, DEBUG=False)
        self.ranking = FillRanking(db, self.CLI_rank, 7, DEBUG=False)
        # Uncomment those line if you implement inbox
        self.FromListener = Listener(db, self.CLI_from, ACTION="Sent", DEBUG=False)#can receive a callback function
        self.toListener = Listener(db, self.CLI_to, ACTION="Received", DEBUG=False)#can receive a callback function
        #callbackDone = threading.Event()

    def UpdateInbox(self):
        global sVar
        if sVar.testing is True: print(f'persona: {sVar.twoFik.Name}')
        if sVar.twoFik.Name is not None:
            if sVar.testing is True: print('entering if in UpdateInbox')
            sVar.inbox.CalculateInbox(sVar.twoFik.Name)


def sLoop():
    global sVar
    if sVar is None:
        sVar = ServerVar()
    if sVar.isAlive is False:
        print("Initialise server")
        # Creates a reference to the messages collection
        sVar.isAlive = init()
    if sVar.lastName != sVar.twoFik.ChatWith:
        if sVar.testing: print("----------------------| updating message query")
        queryChat()
        sVar.lastName = sVar.twoFik.ChatWith
    if sVar.twoFikID != sVar.twoFik.Name:
        if sVar.testing is True: print("launch inbox update")
        #sVar.inbox.CalculateInbox(sVar.twoFik.Name)
        sVar.twoFikID = sVar.twoFik.Name
    #if sVar.isAlive is True:
        #sVar.responseServer.CheckConnection()
    


# Follow 2fik location in real time

def init():
    global sVar
    # start listener on message collection
    queryChat()
    # serverVar.doc_watch = fik_ref.on_snapshot(on_snapshot)
    # create twoFik status object and start listening on it<s in app location
    sVar.twoFik.Follow2fik()
    # Uncomment those line if you implement inbox
    ##sVar.inbox.CalculateInbox(sVar.twoFik.Name)
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
    names_ref = db.collection(u'profiles').document(uid).get()
    return names_ref.get('name')

# Where is 2Fik in the app and which profile is he using
def twofik_location(getID=False):
    # super user to track (in this case Raph for now)
    # identification = 'pX94rzzZRTOfluPkLuRZZKkUmFY2'
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
        sLoop()
    except KeyboardInterrupt:
        if sVar.testing: print('manual interupt')
        sys.exit()

