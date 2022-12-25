# APIのすべての機能を提供するPythonクラス
from fastapi import FastAPI
from firestore_task import collection
from firebase_admin import firestore
import pygeohash as pgh

app = FastAPI()

@app.get("/search") ## 2個エンドポイントつくちゃったから最初の部分が採用される
async def get_name(name: str = None, rating: int = None, price_type: str = None, latitude: str = None, longtitude: str = None):
    li = collection
    if name != None:
        li = li.where('name', '==', name) 
    if rating != None:
        li = li.where('rating', '>', rating).order_by('rating', direction=firestore.Query.DESCENDING)
    if price_type != None:
        li = li.where('price', '==', price_type).order_by('name') # need to create index in price ascending name ascending
    if latitude != None:
        li = li.where('latitude', '==', latitude) 
    if longtitude != None:
        li = li.where('longtitude', '==', longtitude) 
   
    if li != None:
        li = li.get()
        venue = dict()
        key = 0
        for el in li:
            venue[key] = el.to_dict()
            key += 1
        return venue
    else: return  "No match"
