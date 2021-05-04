from firebase_admin import firestore

from td_client import TDClient


class Inbox:
    def __init__(self, database):
        self.db = database
        # self.cli = TDClient('localhost', 1)
        self.persons = {}
        self.maxIndex = 20

    # fills inbox with latest messages
    def CalculateInbox(self, identification):

        # Fetch all the latest messages addressed to the 2fik profile is currently using
        recipient_ref = self.db.collection('messages').where(u'to', u'==', identification).order_by(
            u'time', direction=firestore.Query.DESCENDING).limit(self.maxIndex).stream()

        for msg in recipient_ref:
            user = msg.get('from')
            lastMsg = msg.get('body')
            timestamp = msg.get('time')
            self.addObject(user, lastMsg, timestamp)

        for person in self.persons:
            print(f'{person} -> {self.persons[person][0]} -> {self.persons[person][1]}')

    # def SentMessages(self, identification):
    #     # Fetch all the latest messages sent by the profile 2Fik is currently using
    #     sender_ref = self.db.collection('messages').where(u'from', u'==', identification).order_by(
    #         u'time', direction=firestore.Query.DESCENDING).limit(self.maxIndex).stream()
    #
    #     for msg in sender_ref:
    #         user = msg.get('to')
    #         lastMsg = msg.get('body')
    #         timestamp = msg.get('time')
    #         self.addObject(user, lastMsg, timestamp)
    #
    #     for person in self.persons:
    #         print(f'{person} -> {self.persons[person][0]} -> {self.persons[person][1]}')

    # add passed user and their latest messages
    def addObject(self, user, lastMsg, timestamp):
        obj = [lastMsg, timestamp]
        self.persons[user] = obj
