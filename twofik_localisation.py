import time
import socket
import sys
import firebase_admin
from firebase_admin import credentials, firestore
from td_client import TDClient

class Twofik:
    def __init__(self, cred, db, identification):
        self.credential = cred
        self.db = db
        self.cli = TDClient('localhost', 5784)
        self.twofikID = identification
        self.lastSpeakWith = None
        #firebase_admin.initialize_app(cred,name='2fik_watch')

    def on_snapshot(self, doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            status = doc.to_dict()
            print(f'status: {status}')

    def Follow2fik(self):
        print(f'Following twofik at id: {self.twofikID}')
        collection_ref = self.db.collection("location").document(self.twofikID)
        locationUpdate = collection_ref.on_snapshot(self.on_snapshot)

    def twofik_location(self, getID = False):
        # super user to track (in this case Raph for now)
        #identification = 'uTS21weWNkbggwHu16ScM1Nqart1'
        # firebase database reference
        location_ref = self.db.collection(u'location').document(self.twofikID).get()
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


    