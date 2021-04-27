from firebase_admin import firestore

# from main import db
from td_client import TDClient

db = firestore.client()


class Inbox:
    def __init__(self, identification, user, msg):
        self.cli = TDClient('localhost', 1)
        self.twofikID = identification
        self.person = {user: msg}

    # fill inbox with latest messages
    def CalculateInbox(self, identification):
        # Fetch all the latest messages addressed to the 2fik profile is currently using
        # TODO google.api_core.exceptions.FailedPrecondition: 400 The query requires an index.
        recipient_ref = db.collection('messages').where(u'to', u'==', identification).order_by(
            u'time', direction=firestore.Query.DESCENDING).limit(20).stream()

        for msg in recipient_ref:
            inbox_dictionary = {msg.get('from'), msg.get('body'), msg.get('time')}

        # Fetch all the latest messages sent by the profile 2Fik is currently using
        # TODO google.api_core.exceptions.FailedPrecondition: 400 The query requires an index.
        sender_ref = db.collection('messages').where(u'from', u'==', identification).order_by(
            u'time', direction=firestore.Query.DESCENDING).limit(20).stream()

        for msg in sender_ref:
            inbox_dictionary = {msg.get('to'), msg.get('body'), msg.get('time')}

    def UpdateObj(self, user, lastMsg):
        print('hello')

# check if name is in array.If not add it If it is update last message at the correct index
