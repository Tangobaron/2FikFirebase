from firebase_admin import firestore
from td_client import TDClient


class Inbox:
    def __init__(self, database, cli, DEBUG=False):
        self.db = database
        self.testing = DEBUG
        self.server = cli
        self.persons = {}
        self.maxIndex = 20

    # fills inbox with latest messages
    def CalculateInbox(self, identification):
        # Fetch all the latest messages addressed to the 2fik profile is currently using
        if identification is not None:
            if self.testing is True: print('clearing self.persons')
            self.persons = {}
            recipient_ref = self.db.collection('messages').where(u'to', u'==', identification).order_by(
                u'time', direction=firestore.Query.DESCENDING).limit(self.maxIndex).stream()
            sent_ref = self.db.collection('messages').where(u'from', u'==', identification).order_by(
                u'time', direction=firestore.Query.DESCENDING).limit(self.maxIndex).stream()

            for msg in recipient_ref:
                user = msg.get('from')
                lastMsg = msg.get('body')
                timestamp = msg.get('time')
                if self.testing is True: print(f'user: {user}, lastMsg: {lastMsg}, timestamp: {timestamp}')
                self.addObject(self.persons, user, lastMsg, timestamp)
        
            for msg in sent_ref:
                user = msg.get('to')
                lastMsg = msg.get('body')
                timestamp = msg.get('time')
                if self.testing is True: print(f'user: {user}, lastMsg: {lastMsg}, timestamp: {timestamp}')
                #self.addObject(persons, user, lastMsg, timestamp)
                if user in self.persons:
                    if timestamp > self.persons[user][1]:
                        self.addObject(self.persons,user, lastMsg, timestamp)
                else:
                    self.addObject(self.persons,user, lastMsg, timestamp)
            self.sendToServer(identification)

    def sendToServer(self, identification):
        for key, data in self.persons.items():
            name = str(key)
            lastMsg = str(data[0])
            label = ["2fikID", "name","lastMsg"]
            value = [identification, name, lastMsg]
            self.server.AddToBuffer(label, value)
        self.server.SendMessage()

    # add passed user and their latest messages
    def addObject(self, arr, user, lastMsg, timestamp):
        obj = [lastMsg, timestamp]
        arr[user] = obj
