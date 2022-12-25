import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred) # initialize app to work with firebase

db = firestore.client() # to talk with this db

# Set documents with auto UUIDs(No .document() option)
# # It's perfect combination between Python and Firestore as they both share Key-Value function. 
# data = {
#     name : str,
#     rating : float,
#     url : str,
#     address : str,
#     price_type : str,
#     review_highlights : list,
#     geohash: str,
#     latitude: float,
#     longitude: float
# } 

collection = db.collection('venues')

def add_data(data):
    collection.add(data) # Be mindful that known IDs are preferred in some cases not to add the same data again as designating a specific document avoids create the same Id's document as document name is unique

# Merging data
# db.collectionk('venues').document('venue_name').set({'distance': 'far'}, merge = True) # Must refer to a specific document

# Set documents with known IDs
# db.collection('venues').document('venue_name').set(data)

# Add collection to document
# db.collection('venues').document('venue_name').collection(staffs).add(staff_data)


# ❤️ Set data to document! 
# ❤️ Add data to collection! 

def get_name(rating: int):
    li = collection.where('rating', '>', rating).order_by('rating', direction=firestore.Query.DESCENDING).get()
    # print(li)
    if li != None:
        venue = dict()
        key = 0
        for el in li:
            venue[key] = el.to_dict()
            key += 1
        return venue
    else: return  "No match"
print(get_name(4))