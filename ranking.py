from firebase_admin import firestore

from td_client import TDClient

db = firestore.client()


class Ranking:

    def __init__(self):
        self.not_leaderboard = []
        self.hot_leaderboard = []
        self.cli = TDClient('localhost', 1)

        # Reference to all of 2Fik profiles
        rank_ref = db.collection('profiles').where(u'state', u'==', '2fik').stream()

        # Extracts all the
        for rank in rank_ref:
            name = rank.get('name')
            hot_count = rank.get('hotCount')
            not_count = rank.get('notCount')

            if hot_count > not_count:
                self.hot_leaderboard.append(name, hot_count)
            elif not_count > hot_count:
                self.not_leaderboard.append(name, not_count)
