from firebase_admin import firestore
from td_client import TDClient


class Inbox:
    def __init__(self, database, cli, DEBUG=False):
        self.db = database
        self.testing = DEBUG
        self.server = cli
        self.persons = {}
        self.maxIndex = 20
        self.busy = False
        self.batch = 0

    # fills inbox with latest messages
    def CalculateInbox(self, identification):
        # Fetch all the latest messages addressed to the 2fik profile is currently using
        if identification is not None and self.busy is not True:
            if self.testing is True: print('clearing self.persons')
            self.persons = {}
            self.busy = True
            recipient_ref = self.db.collection('messages').where(u'to', u'==', identification).order_by(
                u'time', direction=firestore.Query.DESCENDING).limit(self.maxIndex).stream()
            sent_ref = self.db.collection('messages').where(u'from', u'==', identification).order_by(
                u'time', direction=firestore.Query.DESCENDING).limit(self.maxIndex).stream()

            for msg in recipient_ref:
                user = msg.get('from')
                lastMsg = msg.get('body')
                timestamp = msg.get('time')

                if self.testing is True: print(f'user: {user}, lastMsg: {lastMsg}, timestamp: {timestamp}')
                self.addObject(self.persons, user, lastMsg, timestamp, "received")
        
            for msg in sent_ref:
                user = msg.get('to')
                lastMsg = msg.get('body')
                timestamp = msg.get('time')

                if self.testing is True: print(f'user: {user}, lastMsg: {lastMsg}, timestamp: {timestamp}')
                if user in self.persons:
                    if timestamp > self.persons[user][1]:
                        self.addObject(self.persons, user, lastMsg, timestamp, "sent")
                else:
                    self.addObject(self.persons, user, lastMsg, timestamp, "sent")
            self.sendToServer(identification)

    def sendToServer(self, identification):
        for key, data in self.persons.items():
            name = str(key)
            lastMsg = str(data[0])
            timeStamp = str(data[1])
            state = str(data[2])
            label = ["2fikID", "id", "name", "lastMsg", "timeStamp", "state", "batch"]
            value = [identification, name, self.get_real_name(name), lastMsg, timeStamp, state, self.batch]
            self.server.AddToBuffer(label, value)
        self.server.SendMessage()
        self.busy = False
        self.batch = self.batch + 1

    def get_real_name(self, uid):
        names_ref = self.db.collection(u'profiles').document(uid).get()
        return names_ref.get('name')

    # add passed user and their latest messages
    @staticmethod
    def addObject(arr, user, lastMsg, timestamp, action):
        obj = [lastMsg, timestamp, action]
        arr[user] = obj
