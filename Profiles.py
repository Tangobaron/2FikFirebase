# Extract the names of the profiles according to their UIDs
def profile_names():
    names_ref = db.collection(u'profiles').get()
    for i in names_ref:
        names = i.get('name')
        uid = i.id
        print(f'{uid} ->  {names}')


# Extract the names of the 2Fik profiles according to their UIDs
def profile_names():
    names_ref = db.collection(u'profiles').get()
    for i in names_ref:
        if i.get('state') == '2fik':
            names = i.get('name')
            uid = i.id
            print(f'{uid} ->  {names}')
