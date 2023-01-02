# APIのすべての機能を提供するPythonクラス
from fastapi import FastAPI
from firestore_task import collection
from firebase_admin import firestore
import pygeohash as pgh
import math
import uvicorn

# 📎 Algorithm to extract geohashes with in XX kilometers from the target point. **********************************
geohashChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
 
class GeoLocation:
    '''
    Class representing a coordinate on a sphere, most likely Earth.
    
    This class is based from the code smaple in this paper:
        http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
        
    The owner of that website, Jan Philip Matuschek, is the full owner of 
    his intellectual property. This class is simply a Python port of his very
    useful Java code. All code written by Jan Philip Matuschek and ported by me 
    (which is all of this class) is owned by Jan Philip Matuschek.
    '''
 
    MIN_LAT = math.radians(-90)
    MAX_LAT = math.radians(90)
    MIN_LON = math.radians(-180)
    MAX_LON = math.radians(180)
    
    EARTH_RADIUS = 6378.1  # kilometers
    
    
    @classmethod
    def from_degrees(cls, deg_lat, deg_lon):
        rad_lat = math.radians(float(deg_lat))
        rad_lon = math.radians(float(deg_lon))
        return GeoLocation(rad_lat, rad_lon, deg_lat, deg_lon)
        
    @classmethod
    def from_radians(cls, rad_lat, rad_lon):
        deg_lat = math.degrees(float(rad_lat))
        deg_lon = math.degrees(float(rad_lon))
        return GeoLocation(rad_lat, rad_lon, deg_lat, deg_lon)
    
    
    def __init__(
            self,
            rad_lat,
            rad_lon,
            deg_lat,
            deg_lon
    ):
        self.rad_lat = float(rad_lat)
        self.rad_lon = float(rad_lon)
        self.deg_lat = float(deg_lat)
        self.deg_lon = float(deg_lon)
        self._check_bounds()
        
    def __str__(self):
        degree_sign= u'\N{DEGREE SIGN}'
        return ("({0:.4f}deg, {1:.4f}deg) = ({2:.6f}rad, {3:.6f}rad)").format(
            self.deg_lat, self.deg_lon, self.rad_lat, self.rad_lon)
        
    def _check_bounds(self):
        if (self.rad_lat < GeoLocation.MIN_LAT 
                or self.rad_lat > GeoLocation.MAX_LAT 
                or self.rad_lon < GeoLocation.MIN_LON 
                or self.rad_lon > GeoLocation.MAX_LON):
            raise Exception("Illegal arguments")
            
    def distance_to(self, other, radius=EARTH_RADIUS):
        '''
        Computes the great circle distance between this GeoLocation instance
        and the other.
        '''
        return radius * math.acos(
                math.sin(self.rad_lat) * math.sin(other.rad_lat) +
                math.cos(self.rad_lat) * 
                math.cos(other.rad_lat) * 
                math.cos(self.rad_lon - other.rad_lon)
            )
            
    def bounding_locations(self, distance, radius=EARTH_RADIUS):
        '''
        Computes the bounding coordinates of all points on the surface
        of a sphere that has a great circle distance to the point represented
        by this GeoLocation instance that is less or equal to the distance argument.
        
        Param:
            distance - the distance from the point represented by this GeoLocation
                       instance. Must be measured in the same unit as the radius
                       argument (which is kilometers by default)
            
            radius   - the radius of the sphere. defaults to Earth's radius.
            
        Returns a list of two GeoLoations - the SW corner and the NE corner - that
        represents the bounding box.
        '''
        
        if radius < 0 or distance < 0:
            raise Exception("Illegal arguments")
            
        # angular distance in radians on a great circle
        rad_dist = distance / radius
        
        min_lat = self.rad_lat - rad_dist
        max_lat = self.rad_lat + rad_dist
        
        if min_lat > GeoLocation.MIN_LAT and max_lat < GeoLocation.MAX_LAT:
            delta_lon = math.asin(math.sin(rad_dist) / math.cos(self.rad_lat))
            
            min_lon = self.rad_lon - delta_lon
            if min_lon < GeoLocation.MIN_LON:
                min_lon += 2 * math.pi
                
            max_lon = self.rad_lon + delta_lon
            if max_lon > GeoLocation.MAX_LON:
                max_lon -= 2 * math.pi
        # a pole is within the distance
        else:
            min_lat = max(min_lat, GeoLocation.MIN_LAT)
            max_lat = min(max_lat, GeoLocation.MAX_LAT)
            min_lon = GeoLocation.MIN_LON
            max_lon = GeoLocation.MAX_LON
        
        # culculate with degree!
        return [ GeoLocation.from_radians(min_lat, min_lon), GeoLocation.from_radians(max_lat, max_lon) , 
            GeoLocation.from_radians(min_lat, max_lon), GeoLocation.from_radians(min_lat, min_lon) ] ## SE, NE, NW, SW
        

def geohashToNum(geohash):
    result = 0
    base = 1
    for i in range(len(geohash) - 1, -1, -1):
        result = result + geohashChars.index(geohash[i]) * base
        base = base * 32
    return result
 
#  Returns from a number (in 32 decimal) to geohash for calculation purposes.
#  @param {Number} num 
def numToGeohash(num):
    result = ''
    while num > 0:
        result = geohashChars[num % 32] + result
        num = math.floor(num / 32);
    
    return result

def getArea(li):
    Min = min(li)
    Max = max(li)
    geohashList = []
    for i in range(Min, Max + 1):
        geohash = numToGeohash(i)
        point = pgh.decode_exactly(geohash)[:2]
        geohashList.append({'geohash': geohash, 'geolocation': GeoLocation.from_degrees(point[0], point[1])})
    return geohashList

def GetHashes(ctr_lat, ctr_lon) :
        loc = GeoLocation.from_degrees(ctr_lat, ctr_lon) # ex: Shibuya station
        distance = 5  # kilometer
        SE_loc, NE_loc, NW_loc, SW_loc = loc.bounding_locations(distance) # return geohash of bounding box points
        SE_hash = pgh.encode(SE_loc.deg_lat, SE_loc.deg_lon, precision = 6)
        NE_hash = pgh.encode(NE_loc.deg_lat, NE_loc.deg_lon, precision = 6)
        NW_hash = pgh.encode(NW_loc.deg_lat, NW_loc.deg_lon, precision = 6)
        SW_hash = pgh.encode(SW_loc.deg_lat, SW_loc.deg_lon, precision = 6)
        li = [geohashToNum(SE_hash), geohashToNum(NE_hash), geohashToNum(NW_hash), geohashToNum(SW_hash)] # 32 digits number to culculate
        # 📋 Test********************************
        # print(loc.distance_to(SE_loc))
        # print(loc.distance_to(NE_loc)) 
        # print(loc.distance_to(NW_loc)) 
        # print(loc.distance_to(SW_loc))
        areaGeohashList = getArea(li)

        # Only geohashes within XX kilometer are extracted.
        hash_in_distance = []
        for el in areaGeohashList:
            if el['geolocation'].distance_to(loc) < distance:
                hash_in_distance.append(el['geohash'])
        return hash_in_distance

        # 📋 Test and Extract to check**********************************
        # with open('eggs.csv', 'w') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(hash_in_distance)   


# ⛏Create API**********************************
app = FastAPI()

@app.get("/search")
async def get_name(name: str = None, rating: float = None, price_type: str = None, latitude: str = None, longtitude: str = None):
    queries = collection
    if name != None:
        queries = queries.where('name', '==', name) 
    if rating != None:
        queries = queries.where('rating', '>', rating).order_by('rating', direction=firestore.Query.DESCENDING)
    if price_type != None:
        queries = queries.where('price', '==', price_type).order_by('name')
    if latitude != None and longtitude != None:
        # Returns the set of geohashes within 5 km of an arbitrary latitude and longitude in descending order.
        hashes_in_distance = GetHashes(latitude, longtitude)
        correct_query_results = []
        while hashes_in_distance:
            hashes_in_distance_sliced = hashes_in_distance[:10]
            del hashes_in_distance[:10]
            correct_query_results.append(queries.where('geohash', 'in' , hashes_in_distance_sliced))
        queries = correct_query_results
        
    if type(queries) != list:
        queries = [queries]

    if queries != None:
        print(queries)
        venue = []
        key = 0
        for query in queries:
            query = query.get()
            for document in query:
                venue.append(document.to_dict())
                key += 1
        # Sort by shortest distance from center location
        if latitude != None and longtitude != None:
            venue = sorted(venue, 
                key = lambda item: 
                    (GeoLocation.from_degrees(item['latitude'], item['longtitude']).distance_to(GeoLocation.from_degrees(latitude, longtitude))))
        return venue
    else: return  "No match"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)