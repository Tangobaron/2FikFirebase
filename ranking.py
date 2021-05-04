from firebase_admin import firestore

from td_client import TDClient


class Ranking:

    def __init__(self, database):
        self.db = database
        self.not_leaderboard = []
        self.hot_leaderboard = []
        # self.cli = TDClient('localhost', 1)

        # Reference to all of 2Fik profiles
        rank_ref = self.db.collection('profiles').where(u'state', u'==', '2fik').stream()

        # Extracts all the
        # TODO add logic to make sure people with the same amount of votes are organized depending on the amount of opposite vote and alphabetical order

        for rank in rank_ref:
            name = rank.get('name')
            hot_count = rank.get('hotCount')
            not_count = rank.get('notCount')

            if hot_count > not_count:
                hot_dict = {name, hot_count}
                self.hot_leaderboard.append(hot_dict)
            elif not_count > hot_count:
                not_dict = {name, not_count}
                self.not_leaderboard.append(not_dict)

        print(f'hot leaderboard -> {self.hot_leaderboard}')
        print(f'not leaderboard -> {self.not_leaderboard}')
