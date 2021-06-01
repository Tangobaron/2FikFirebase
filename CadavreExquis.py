from firebase_admin import firestore
from td_client import TDClient
from snapshot_class import Snapshot as Listener


class CadavreExquis:
    def __init__(self, database, cli, DEBUG=False, length=15):
        self.db = database
        self.testing = DEBUG
        self.server = cli
        self.collection = self.db.collection('messages')
        self.nbrToQuery = length
        self.initialQuery()
        self.docWatch = None

    def initialQuery(self):
        query_ref = self.collection.limit_to_last(self.nbrToQuery).get()
        for doc in query_ref:
            sender = doc.get("from")
            msg = doc.get("body")
            label = ["time", "Message"]
            value = [doc.get("time"), msg]
            self.server.AddToBuffer(label, value)
        self.server.SendMessage()
        self.WatchUpdate()

    def WatchUpdate(self):
        if self.testing is True: print("WatchUpdate...")
        watchquery = self.collection.limit_to_last(self.nbrToQuery)
        self.docWatch = watchquery.on_snapshot(self.on_snapshot)

    def on_snapshot(self, doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                doc = change.document
                msg = doc.get("body")
                label = ["time", "Message"]
                value = [doc.get("time"), msg]
                self.server.AddToBuffer(label, value)
        self.server.SendMessage()

    def get_real_name(self, uid):
        names_ref = self.db.collection(u'profiles').document(uid).get()
        return names_ref.get('name')

