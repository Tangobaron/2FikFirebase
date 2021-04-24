import socket
import sys
import firebase_admin
from firebase_admin import credentials, firestore
from td_client import TDClient

class Twofik:
    def __init__(self, cred, db, identification):
        self.credential = cred
        self.database = db
        self.cli = TDClient('localhost', 5784)
        self.twofikID = identification

    def Follow2fik(self):
        print(f'Following twofik at id: {self.twofikID}')

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
