from main import db


class Ranking:
    def __init__(self, name, uid):
        self.name = name
        self.uid = uid

    # Returns the entire list of user profiles
    def Users_profile_names(self):
        names_ref = db.collection(u'profiles').where(u'state', u'!=', u'2fik').stream()
        for name in names_ref:
            users_list = name.get('name')
            return users_list

    # Returns the entire list of 2Fik profiles
    def Twofik_profile_names(self):
        names_ref = db.collection(u'profiles').where(u'state', u'==', u'2fik').stream()
        for name in names_ref:
            twofik_list = name.get('name')
            return twofik_list

    # Gets a single real name from a UID
    def Get_real_name(uid):
        names_ref = db.collection(u'profiles').where(u'name', u'==', uid).stream()
        for dictionary in names_ref:
            name = dictionary.get('name')
            return name
