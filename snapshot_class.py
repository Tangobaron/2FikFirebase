import socket
import sys
import firebase_admin
import threading

from td_client import TDClient
from firebase_admin import credentials, firestore
class Snapshot:
    def __init__(self, database, TDClient, ACTION = None, DEBUG = False):
        self.testing = DEBUG
        self.db = database
        self.initialQuery = False
        self.client = TDClient
        self.callbackDone = threading.Event()
        self.docWatch = None
        self.action = ACTION
    
    def get_real_name(self, uid):
        names_ref = self.db.collection(u'profiles').get()
        for name in names_ref:
            if uid == name.id:
                return name.get('name')

    def StartListening(self, doc):
        self.docWatch = doc.on_snapshot(self.on_snapshot)

    def SetNewListener(self, doc):
        if self.docWatch is not None:
            if self.testing: print("remove listener after the callback trigger")
            self.callbackDone.wait(timeout=30)
            self.docWatch.unsubscribe()
            self.initialQuery = False
        self.docWatch = doc.on_snapshot(self.on_snapshot)

    def on_snapshot(self, doc_snapshot, changes, read_time):
        #need to be last 2 line of this function 
        if self.testing: print("finished query")
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
            messages = doc.to_dict()
            #print(f'messages: {messages}')
            sender = self.get_real_name(messages.get('from'))
            recipientID = messages.get('to')
            senderID = messages.get('from')
            recipient = self.get_real_name(recipientID)
            #print(f'recipient: {recipient}')
            time_of_reception = self.formatTime(messages.get('time'))
            text = messages.get('body')
            nameList = ["sender", "recipient", "recipientID", "senderID", "time", "text", "action"]
            dataList = [str(sender), str(recipient), str(recipientID), str(senderID), str(time_of_reception), str(text), str(self.action)]
            self.client.AddToBuffer(nameList, dataList)
            if self.testing: print(f"sender:     {sender}")
            if self.testing: print(f"recipient:  {recipient}")
            if self.testing: print(f"time:       {time_of_reception}")
            if self.testing: print(f"text:       {text}")
            if self.testing: print('_____________________________________________________________________________________________________________')
        self.initialQuery = True
        self.client.SendMessage()
        self.callbackDone.set()
    
        
    def watch_updates(self, changes):
        for change in changes:
            if self.testing: print(f'changeType: {change.type.name}')
            if change.type.name == 'ADDED':
                doc = change.document
                #doc = change.after()
                messages = doc.to_dict()
                if self.testing: print('__________________________________________________\\\\_______________________________________________________')
                if self.testing: print(f'messages: {messages}')
                if self.testing: print('__________________________________________________\\\\\______________________________________________________')
                sender = self.get_real_name(messages.get('from'))
                recipientID = messages.get('to')
                senderID = messages.get('from')
                recipient = self.get_real_name(recipientID)
                #print(f'recipient: {recipient}')
                time_of_reception = self.formatTime(messages.get('time'))
                text = messages.get('body')
                nameList = ["sender", "recipient", "recipientID", "senderID", "time", "text", "action"]
                dataList = [str(sender), str(recipient), str(recipientID), str(senderID), str(time_of_reception), str(text), str(self.action)]
                self.client.AddToBuffer(nameList, dataList)
        self.client.SendMessage()
        self.callbackDone.set()