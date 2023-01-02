# Library: Requests, Beautifulsoup
import requests 
from bs4 import BeautifulSoup
from time import sleep
from firestore_task import add_data
import pygeohash as pgh

url = 'https://www.yelp.com/search?cflt=restaurants&find_loc=Sydney%20New%20South%20Wales'
query = '&start='
value = 10

# 今回は、エラーが起きた場合は、エラーを無視するのでpassと記述します。
# ちなみに、passは、特に何も処理を実行しない時に使用します。
class Scr():
    def __init__(self, url, query, value):
        self.url = url
        self.query = query
        self.page_num = (value - 1) * 10 + 10 # Cauz I am scraping 10 pages, I want "&start=90" so that the number of elements is 100.
        self.all_content = []
    def geturl(self):
        for page in range(self.page_num): # 0 ~ 99
            print(page)
            if page%10 == 0:
                url = self.url + self.query + str(page//10*10)
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c, "lxml") # lxml: the fast parser. Get the Collection of restaurant URL.
                urls_restaurant = soup.select(".css-8dlaw4") # 💔 selection is not sorted
                for url in urls_restaurant:
                    urls_restaurant[urls_restaurant.index(url)] = url.get('href')

            # *** Get in specific restaurant page ***
            temp = dict()
            data = dict()
            restaurant_url = 'https://www.yelp.com/' + urls_restaurant[page%10]
            r_restaurant = requests.get(restaurant_url)
            c_restaurant = r_restaurant.content
            soup_restaurant = BeautifulSoup(c_restaurant, "lxml") # Get the specific restaurant page.

            # restaurant_name
            if (restaurant_name := soup_restaurant.select_one("body > yelp-react-root > div:nth-child(1) > div.photoHeader__09f24__nPvHp.border-color--default__09f24__NPAKY > div.photo-header-content-container__09f24__jDLBB.border-color--default__09f24__NPAKY > div.photo-header-content__09f24__q7rNO.padding-r2__09f24__ByXi4.border-color--default__09f24__NPAKY > div > div > div.headingLight__09f24__N86u1.margin-b1__09f24__vaLrm.border-color--default__09f24__NPAKY")) != None:
                restaurant_name = restaurant_name.text
            else: restaurant_name = None
            temp["restaurant_name"] = data["name"] = restaurant_name

            # restaurant_rating
            if (restaurant_rating := soup_restaurant.select_one("body > yelp-react-root > div:nth-child(1) > div.photoHeader__09f24__nPvHp.border-color--default__09f24__NPAKY > div.photo-header-content-container__09f24__jDLBB.border-color--default__09f24__NPAKY > div.photo-header-content__09f24__q7rNO.padding-r2__09f24__ByXi4.border-color--default__09f24__NPAKY > div > div > div.arrange__09f24__LDfbs.gutter-1-5__09f24__vMtpw.vertical-align-middle__09f24__zU9sE.margin-b2__09f24__CEMjT.border-color--default__09f24__NPAKY > div:nth-child(1) > span > div").get('aria-label')) != None:
                restaurant_rating = restaurant_rating[:restaurant_rating.find(' ')]
            else: restaurant_rating = None
            temp["restaurant_rating"] = data["rating"] = float(restaurant_rating)

            # url
            data["url"] = restaurant_url

            # restaurant_address
            if (restaurant_address := soup_restaurant.select_one("address")) != None:
                restaurant_address = restaurant_address.text
            else: restaurant_address = None
            temp["restaurant_address"] = data["address"] = restaurant_address

            # price_type
            if (price_type := soup_restaurant.select_one("body > yelp-react-root > div:nth-child(1) > div.photoHeader__09f24__nPvHp.border-color--default__09f24__NPAKY > div.photo-header-content-container__09f24__jDLBB.border-color--default__09f24__NPAKY > div.photo-header-content__09f24__q7rNO.padding-r2__09f24__ByXi4.border-color--default__09f24__NPAKY > div > div > span:nth-child(4) > span")) != None:
                price_type = price_type.text
            else: price_type = None
            temp["price_type"] = data["price"] = price_type[:price_type.find(' ')]

            # review_highlights
            review_highlights = soup_restaurant.select(".comment__09f24__gu0rG")
            if len(review_highlights) >= 3:
                review_highlights = review_highlights[:3]
                for i in review_highlights:
                    review_highlights[review_highlights.index(i)] = i.text
            elif (review_highlights := soup_restaurant.select("div.border-color--default__09f24__NPAKY > p.css-2sacua")) != None:
                for rev in review_highlights:
                    review_highlights[review_highlights.index(rev)] = rev.text
            else:
                review_highlights = None
            temp["review_highlights"] = data["review"] = review_highlights
            
            # get latitude and longtitude and geohash
            if (geo_url := soup_restaurant.select_one('#location-and-hours > section > div.arrange__09f24__LDfbs.gutter-4__09f24__dajdg.border-color--default__09f24__NPAKY > div:nth-child(1) > div > a > div > img').get('src')) != None:
                lat, lon = geo_url.split('&center=')[1].split('&markers=')[0].split('%2C') # %2C is a comma in ASCII
                try:
                    lat, lon = float(lat), float(lon)
                except ValueError:
                    lat, lon = geo_url.split('&center=')[1].split('&signature=')[0].split('%2C') # %2C is a comma in ASCII
                    lat, lon = float(lat), float(lon)
                # print(lat, lon)
            else:
                lat, lon = None, None
                geohash = None
            data["geohash"] = pgh.encode(lat, lon, precision = 6)
            data["latitude"], data["longtitude"] = lat, lon
            
            self.all_content.append(temp)
            add_data(data)

            # Rest to reduce server load.
            sleep(1)
        return self.all_content

if __name__ == '__main__':
    sc = Scr(url, query, value)
    print(sc.geturl())