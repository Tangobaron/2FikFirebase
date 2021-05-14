# import tabulate
import firebase_admin
import threading
from td_client import TDClient


class Ranking:

    def __init__(self, database, nbrQuery, DEBUG=False):
        self.testing = DEBUG
        self.db = database
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
        rank_ref = self.db.collection('profiles').where(u'state', u'==', '2fik').stream()
        for rank in rank_ref:
            name = rank.get('name')
            uid = rank.id
            hot_count = rank.get('hotCount')
            not_count = rank.get('notCount')

            hot_dict = {'UID': uid, 'Name': name, 'Hot Count': hot_count}
            self.hot_leaderboard.append(hot_dict)
            self.hot_leaderboard.sort(key=lambda i: i['Hot Count'], reverse=True)
            self.hot_leaderboard = self.hot_leaderboard[:self.list_size]

            not_dict = {'UID': uid, 'Name': name, 'Not Count': not_count}
            self.not_leaderboard.append(not_dict)
            self.not_leaderboard.sort(key=lambda i: i['Not Count'], reverse=True)
            self.not_leaderboard = self.not_leaderboard[:self.list_size]

        print(f'Hot Leaderboard -> {self.hot_leaderboard}')
        print(f'Not Leaderboard -> {self.not_leaderboard}')
