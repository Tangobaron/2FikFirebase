from td_client import TDClient


class Ranking:

    def __init__(self, database):
        self.db = database
        self.not_leaderboard = []
        self.hot_leaderboard = []
        self.list_size = 7
        # self.cli = TDClient('localhost', 1)

        # Reference to all of 2Fik profiles
        rank_ref = self.db.collection('profiles').where(u'state', u'==', '2fik').stream()

        # Extract all the names, hotCount and notCount of every 2Fik profiles
        for rank in rank_ref:
            name = rank.get('name')
            uid = rank.id
            hot_count = rank.get('hotCount')
            not_count = rank.get('notCount')

            if hot_count > not_count:
                hot_dict = {'UID': uid, 'Name': name, 'Hot Count': hot_count}
                self.hot_leaderboard.append(hot_dict)
                self.hot_leaderboard.sort(key=lambda i: i['Hot Count'], reverse=True)
                self.hot_leaderboard = self.hot_leaderboard[:self.list_size]

            elif not_count > hot_count:
                not_dict = {'UID': uid, 'Name': name, 'Not Count': not_count}
                self.not_leaderboard.append(not_dict)
                self.not_leaderboard.sort(key=lambda i: i['Not Count'], reverse=True)
                self.not_leaderboard = self.not_leaderboard[:self.list_size]

        print(f'Hot Leaderboard -> {self.hot_leaderboard}')
        print(f'Not Leaderboard -> {self.not_leaderboard}')
