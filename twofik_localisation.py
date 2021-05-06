import time
import socket
import sys
import firebase_admin
from firebase_admin import credentials, firestore
from td_client import TDClient

class Twofik:
    def __init__(self, cred, db, identification, DEBUG = False):
        self.testing = DEBUG
        self.credential = cred
        self.db = db
        # self.cli = TDClient('localhost', 5784)
        self.twofikID = identification
        self.lastSpeakWith = None
        #variable related to 2fik location
        self.Name = None
        self.personaID = None
        self.VisitedProfile = None
        self.ChatWith = None
        self.BodyLocation = None
        self.PanelLocation = None

    def on_snapshot(self, doc_snapshot, changes, read_time):
        if self.testing: print("enter on snapshot")
        for doc in doc_snapshot:
            status = doc.to_dict()
            body = status.get('body')
            panel = status.get('panel')
            if self.testing: print(f'status: {status}')
            #-------------name---------------
            name = status.get('profile')
            if name != self.Name:
                self.ChatWith = None
            self.Name = name
            if self.testing: print(f'Name: {self.Name}')
            #-----------location-------------
            self.BodyLocation = body.get('state')
            self.PanelLocation = panel.get('state')
            if self.testing: print(f'BodyLocation: {self.BodyLocation}')
            if self.testing: print(f'PanelLocation: {self.PanelLocation}')
            #---------visit profile----------
            body_profile = body.get('profile')
            if body_profile is not None:
                self.VisitedProfile = body_profile
            if self.testing: print(f'body_profile: {self.VisitedProfile}')
            #-----------chat with-------------
            if panel.get('state') == "chat":
                profile = panel.get('profile')
                self.ChatWith = profile
            if self.testing: print(f'ChatWith: {self.ChatWith}')
        self.sendUpdate()
    
    def get_real_name(self, uid):
        names_ref = self.db.collection(u'profiles').get()
        for name in names_ref:
            if uid == name.id:
                return name.get('name')

    def sendUpdate(self):
        nameList = ["Twofik_ID", "Name", "Body_Location", "Panel_Location", "Visited_Profile", "Chat_With", "Chat_ID"]
        dataList = [str(self.Name), str(self.get_real_name(self.Name)), str(self.BodyLocation), str(self.PanelLocation), str(self.VisitedProfile), str(self.get_real_name(self.ChatWith)), str(self.ChatWith)]
        # self.cli.AddToBuffer(nameList, dataList)
        # self.cli.SendMessage()

    def Follow2fik(self):
        if self.testing: print(f'Following twofik at id: {self.twofikID}')
        collection_ref = self.db.collection("location").document(self.twofikID)
        locationUpdate = collection_ref.on_snapshot(self.on_snapshot)

    def twofikLocation(self, getID = False):
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
        if self.testing: print('______________________________________________________________________________')
        if self.testing: print(f'profile used : {profile_selected}')
        if self.testing: print(body_state)
        if self.testing: print(panel_state)
        if self.testing: print('______________________________________________________________________________')
        if getID == True:
            return profile_selected
        else:
            return get_real_name(profile_selected)


    