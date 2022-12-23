# Library: Requests, Beautifulsoup
import requests # to use: $ pip3 install requests
from bs4 import BeautifulSoup # to use: $ pip3 install beautifulsoup4
# to avoid overwhelming server, operate scraping timing
from time import sleep
from firestore_task import add_data

url = 'https://www.yelp.com/search?cflt=restaurants&find_loc=Sydney%20New%20South%20Wales'
query = '&start='
page_num = 10

# 続いて、もしエラーが起きた場合にはexcept:の下に処理を実行します。
# 今回は、エラーが起きた場合は、エラーを無視するのでpassと記述します。
# ちなみに、passは、特に何も処理を実行しない時に使用します。
class Scr():
    def __init__(self, url, query, page_num):
        self.url = url
        self.query = query
        self.page_num = (page_num - 1) * 10 + 10 # １０ページスクレイピングするなら&start=90まで欲しい & 要素数は１００
        # self.all_content = []
    def geturl(self):
        for page in range(self.page_num): # 0 ~ 99
            print(page)
            if page%10 == 0:
                url = self.url + self.query + str(page//10*10)
                r = requests.get(url) #Webページへ移動する前に、次の処理に行かないように、time.sleep(3)で、3秒待機する記述 ->　本当にこういう意味かチェック
                c = r.content
                soup = BeautifulSoup(c, "lxml") # the fast parser. to use: $ pip3 install lxml
                urls_restaurant = soup.select(".css-8dlaw4")
                for url in urls_restaurant:
                    urls_restaurant[urls_restaurant.index(url)] = url.get('href')

            # *** specific restaurant page ***
            temp = dict()
            r_restaurant = requests.get('https://www.yelp.com/' + urls_restaurant[page%10])
            c_restaurant = r_restaurant.content
            soup_restaurant = BeautifulSoup(c_restaurant, "lxml") # the fast parser. to use: $ pip3 install lxml


            if (restaurant_name := soup_restaurant.select_one(".headingLight__09f24__N86u1 > h1")) != None:
                restaurant_name = restaurant_name.text
            else: restaurant_name = None

            if (restaurant_rating := soup_restaurant.select_one(".five-stars__09f24__mBKym").get('aria-label')) != None:
                restaurant_rating = restaurant_rating[:restaurant_rating.find(' ')]
            else: restaurant_rating = None

            if (restaurant_address := soup_restaurant.select_one("address")) != None:
                restaurant_address = restaurant_address.text
            else: restaurant_address = None

            if (price_type := soup_restaurant.select_one(".css-1ir4e44")) != None:
                price_type = price_type.text
            else: price_type = None

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

            temp["restaurant_name"] = restaurant_name
            temp["restaurant_rating"] = restaurant_rating
            temp["restaurant_address"] = restaurant_address
            temp["price_type"] = price_type
            temp["review_highlights"] = review_highlights
            
            # self.all_content.append(temp)
            add_data(temp)
            sleep(1)

        return self.all_content

if __name__ == '__main__':
    sc = Scr(url, query, page_num)
    print(sc.geturl())