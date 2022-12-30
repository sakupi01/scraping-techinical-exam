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