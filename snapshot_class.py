import socket
import sys
import firebase_admin
import threading

from td_client import TDClient
from firebase_admin import credentials, firestore
class Snapshot:
    def __init__(self, database, TDClient, ACTION = None, callback = None, DEBUG = False):
        self.testing = DEBUG
        self.db = database
        self.initialQuery = False
        self.client = TDClient
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

    def returnStream(self):
        print("returnStream")

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
            #print(f'messages: {messages}')
            #sender = self.get_real_name(messages.get('from'))
            #sender = "testSender"
            #recipientID = messages.get('to')
            #senderID = messages.get('from')
            #recipient = self.get_real_name(recipientID)
            target = ""
            if(self.action == "Received"):
                target = messages.get('from')
            elif(self.action == "Sent"):
                target = messages.get('to')
            #print(f'recipient: {recipient}')
            time_of_reception = self.formatTime(messages.get('time'))#self.formatTime(messages.get('time'))
            text = messages.get('body')
            nameList = ["target", "time", "text", "action"]
            dataList = [target, str(time_of_reception), text, self.action]
            self.client.AddToBuffer(nameList, dataList)
            #self.client.SendMessage()
            #if self.testing: print(f"sender:     {sender}")
            #if self.testing: print(f"recipient:  {recipient}")
            #if self.testing: print(f"time:       {time_of_reception}")
            #if self.testing: print(f"text:       {text}")
            #if self.testing: print('_____________________________________________________________________________________________________________')
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
                #doc = change.after()
                messages = doc
                if self.testing: print('__________________________________________________\\\\_______________________________________________________')
                if self.testing: print(f'messages: {messages}')
                if self.testing: print('__________________________________________________\\\\\______________________________________________________')
                #sender = self.get_real_name(messages.get('from'))
                #recipientID = messages.get('to')
                #senderID = messages.get('from')
                #recipient = self.get_real_name(recipientID)
                #print(f'recipient: {recipient}')
                target = ""
                if(self.action == "Received"):
                    target = messages.get('from')
                elif(self.action == "Sent"):
                    target = messages.get('to')
                time_of_reception = self.formatTime(messages.get('time'))
                text = messages.get('body')
                nameList = ["target", "time", "text", "action"]
                dataList = [target, str(time_of_reception), text, self.action]
                self.client.AddToBuffer(nameList, dataList)
                self.client.SendMessage()
        #self.client.SendMessage()
        self.callbackDone.set()