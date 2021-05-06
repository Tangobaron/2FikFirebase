import tabulate

from td_client import TDClient


class Ranking:

    def __init__(self, database):
        self.db = database
        self.not_leaderboard = []
        self.hot_leaderboard = []
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
                hot_dict = {'uid': uid, 'name': name, 'hot_count': hot_count}
                self.hot_leaderboard.append(hot_dict)
                self.hot_leaderboard.sort(key=lambda i: i['hot_count'], reverse=True)
            elif not_count > hot_count:
                not_dict = {'uid': uid, 'name': name, 'not_count': not_count}
                self.not_leaderboard.append(not_dict)
                self.not_leaderboard.sort(key=lambda i: i['not_count'], reverse=True)

        header_hot = self.hot_leaderboard[0].keys()
        rows_hot = [x.values() for x in self.hot_leaderboard]
        print(tabulate.tabulate(rows_hot, header_hot))
        print('------------------------------------------')

        header_not = self.not_leaderboard[0].keys()
        rows_not = [x.values() for x in self.not_leaderboard]
        print(tabulate.tabulate(rows_not, header_not))
