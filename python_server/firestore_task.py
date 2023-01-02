import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred) # initialize app to work with firebase

db = firestore.client() # to talk with this db

collection = db.collection('venues')