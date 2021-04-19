
db = firestore.client()

# Creates a reference to the collection profiles to fetch users names
names_ref = db.collection('profiles').order_by('time', direction=firestore.Query.DESCENDING).limit(3)
user_name = names_ref.get('name')