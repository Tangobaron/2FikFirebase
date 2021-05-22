import socket
import sys
import firebase_admin
import threading

from td_client import TDClient
from firebase_admin import credentials, firestore


class Snapshot:
    def __init__(self, database, TD_Client, ACTION=None, callback=None, DEBUG=False):
        self.testing = DEBUG
        self.db = database
        self.initialQuery = False
        self.client = TD_Client
        self.callbackDone = threading.Event()
        self.extCallback = callback
        self.docWatch = None
        self.action = ACTION
    
    def get_real_name(self, uid):
        names_ref = self.db.collection(u'profiles').document(uid).get()
        return names_ref.get('name')

    def SetNewListener(self, doc):
        if self.docWatch is not None:
            if self.testing: print("remove listener after the callback trigger")
            self.callbackDone.wait(timeout=30)
            if self.testing: print("finish removing")
            self.docWatch.unsubscribe()
            self.initialQuery = False
        self.docWatch = doc.on_snapshot(self.on_snapshot)

    def on_snapshot(self, doc_snapshot, changes, read_time):
        #need to be last 2 line of this function 
        if self.testing: print("finished query")
        if self.extCallback is not None:
            self.extCallback()
        if self.initialQuery is False:
            self.query_init(doc_snapshot)
        else:
            self.watch_updates(changes)
    
    def formatTime(self, time):
        string = str(time)
        trimed = string.split('+')[0]
        formatTime = trimed.replace(" ", "")
        formatTime = formatTime.replace(":", "")
        formatTime = formatTime.replace(".", "")
        formatTime = formatTime.replace("-", "")
        return formatTime

    def query_init(self, doc_snapshot):

        for doc in doc_snapshot:
            if self.testing: print('newEntry')
            messages = doc
            target = ""
            if self.action == "Received":
                target = messages.get('from')
            elif self.action == "Sent":
                target = messages.get('to')
            time_of_reception = self.formatTime(messages.get('time'))
            text = messages.get('body')
            nameList = ["target", "time", "text", "action"]
            dataList = [target, str(time_of_reception), text, self.action]
            self.client.AddToBuffer(nameList, dataList)

        if self.testing: print('finish query')
        self.initialQuery = True
        if self.testing: print('befor send')
        self.client.SendMessage()
        if self.testing: print('after send')
        self.callbackDone.set()

    def watch_updates(self, changes):
        for change in changes:
            if self.testing: print(f'changeType: {change.type.name}')
            if change.type.name == 'ADDED':
                doc = change.document
                messages = doc
                if self.testing: print('_____________________________________________________________________________________________________________')
                if self.testing: print(f'messages: {messages}')
                if self.testing: print('_____________________________________________________________________________________________________________')

                target = ""
                if self.action == "Received":
                    target = messages.get('from')
                elif self.action == "Sent":
                    target = messages.get('to')
                time_of_reception = self.formatTime(messages.get('time'))
                text = messages.get('body')
                nameList = ["target", "time", "text", "action"]
                dataList = [target, str(time_of_reception), text, self.action]
                self.client.AddToBuffer(nameList, dataList)
                self.client.SendMessage()
        self.callbackDone.set()