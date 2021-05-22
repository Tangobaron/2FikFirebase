# import tabulate
import firebase_admin
import threading
from td_client import TDClient


class Ranking:

    def __init__(self, database, client, nbrQuery, DEBUG=False):
        self.testing = DEBUG
        self.db = database
        self.CLI = client
        self.not_leaderboard = []
        self.hot_leaderboard = []
        self.list_size = nbrQuery
        self.docWatch = None
        # self.cli = TDClient('localhost', 1)

        # Reference to all of 2Fik profiles
        ref = self.db.collection('ranks')
        # Extract all the names, hotCount and notCount of every 2Fik profiles
        self.docWatch = ref.on_snapshot(self.on_snapshot)

    def on_snapshot(self, doc_snapshot, changes, read_time):
        self.not_leaderboard = []
        self.hot_leaderboard = []
        rank_ref = self.db.collection('profiles').where(u'state', u'==', '2fik').stream()
        for rank in rank_ref:
            name = rank.get('name')
            uid = rank.id
            hot_count = rank.get('hotCount')
            not_count = rank.get('notCount')
            time_stamp = rank.get('time')

            hot_dict = {'UID': uid, 'Name': name, 'Hot Count': hot_count, 'Time': time_stamp}
            self.hot_leaderboard.append(hot_dict)
            self.hot_leaderboard.sort(key=lambda i: i['Hot Count'], reverse=True)
            self.hot_leaderboard = self.hot_leaderboard[:self.list_size]

            not_dict = {'UID': uid, 'Name': name, 'Not Count': not_count, 'Time': time_stamp}
            self.not_leaderboard.append(not_dict)
            self.not_leaderboard.sort(key=lambda i: i['Not Count'], reverse=True)
            self.not_leaderboard = self.not_leaderboard[:self.list_size]
        self.composeMessage()
        if self.testing is True: print(f'Hot Leaderboard -> {self.hot_leaderboard}')
        if self.testing is True: print(f'Not Leaderboard -> {self.not_leaderboard}')

    def composeMessage(self):
        for rank in self.not_leaderboard:
            labels = ["ID", "name", "count", "type"]
            datas = [rank.get("UID"), rank.get("Name"), rank.get("Not Count"), "Not"]
            self.CLI.AddToBuffer(labels, datas)
        for rank in self.hot_leaderboard:
            labels = ["ID", "name", "count", "type"]
            datas = [rank.get("UID"), rank.get("Name"), rank.get("Hot Count"), "Hot"]
            self.CLI.AddToBuffer(labels, datas)
        self.CLI.SendMessage()
