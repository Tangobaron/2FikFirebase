from firebase_admin import firestore

from td_client import TDClient

db = firestore.client()


class Inbox:
    def __init__(self):
        self.cli = TDClient('localhost', 1)
        self.persons = {}
        self.maxIndex = 20

    # fill inbox with latest messages
    def CalculateInbox(self, identification):

        # Fetch all the latest messages addressed to the 2fik profile is currently using
        # TODO google.api_core.exceptions.FailedPrecondition: 400 The query requires an index.
        recipient_ref = db.collection('messages').where(u'to', u'==', identification).order_by(
            u'time', direction=firestore.Query.DESCENDING).limit(self.maxIndex).stream()

        for msg in recipient_ref:
            user = msg.get('to')
            lastMsg = msg.get('body')
            if user in self.persons:
                updateObj(user, lastMsg)
            elif user not in self.persons:
                addObject(user, lastMsg)
            else:
                print("sender error")

        # Fetch all the latest messages sent by the profile 2Fik is currently using
        # TODO google.api_core.exceptions.FailedPrecondition: 400 The query requires an index.
        sender_ref = db.collection('messages').where(u'from', u'==', identification).order_by(
            u'time', direction=firestore.Query.DESCENDING).limit(self.maxIndex).stream()

        for msg in sender_ref:
            user = msg.get('to')
            lastMsg = msg.get('body')
            if user in self.persons:
                updateObj(user, lastMsg)
            elif user not in self.persons:
                addObject(user, lastMsg)
            else:
                print("sender error")


# add passed user and their latest messages
def addObject(self, user, lastMsg):
    self.persons.add(user, lastMsg)


# updates the passed user's latest message
def updateObj(self, user, lastMsg):
    self.persons[user] = lastMsg
