import urllib.request as url
from bs4 import BeautifulSoup as bs
from dateutil import parser
import re
import time

class Hotel:
    def __init__(self, date):
        self.name = ""
        self.date = date
        self.available = 0
        self.max_rent = 0
        self.rent = 0
        self.rating = 0
        self.guest_rating = 0
        self.address = ""
        self.zip_code = ""
        self.desc = ""
        self.wifi = 0
        self.breakfast = 0
        self.capacity = 0
        self.swimming_pool = 0

    def print(self):
        print(self.__dict__)

    def get_csv(self):
        output = [str(self.__dict__[a]) for a in self.__dict__]
        output = ":".join(output)
        return output

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent': user_agent}

hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://cssspritegenerator.com',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

dates = 'Nov 29 2017:\
Nov 30 2017:\
Dec 1 2017:\
Dec 2 2017:\
Dec 3 2017:\
Dec 4 2017:\
Dec 5 2017:\
Dec 6 2017:\
Dec 7 2017:\
Dec 8 2017'

dates = dates.split(':')

for i, date in enumerate(dates):
    dates[i] = parser.parse(date)

# Columbus
# Arlington
# Buffalo


def get_search_url(date):
    # Edit this url for updates
    search_url = "https://www.hotels.com/search.do?resolved-location=CITY%3A1489699%3AUNKNOWN%3AUNKNOWN&destination-id=1489699&q-destination=Asheville,%20North%20Carolina,%20United%20States%20of%20America&q-check-in=" \
                 + date + \
                 "&q-check-out=2017-12-06&q-rooms=1&q-room-0-adults=2&q-room-0-children=0"
    return search_url


def get_hotel_details(hotel_url, date):

    try:
        page_url = hotel_url

        request = url.Request(page_url, None, hdr)
        response = url.urlopen(request)
        data = response.read()

        soup = bs(data, 'html.parser')

        # Hotel data
        hotel = Hotel(date)
        # Hotel name
        hotel.name = soup.find('div', attrs={'class': 'vcard'})
        hotel.name = hotel.name.find('h1').text

        # Price
        rent = soup.find('div', attrs={'class': 'price'})
        hotel.max_rent = rent.find('del', attrs={'class': 'old-price'})
        if hotel.max_rent is not None:
            hotel.max_rent = hotel.max_rent.text
        hotel.rent = rent.find('span', attrs={'class': 'current-price'}).text

        # rating
        rating = soup.find('span', attrs={'class': "star-rating-text"})
        rating = rating.find('span').text.replace("stars", "")
        hotel.rating = rating

        # Guest Rating
        gr = soup.find('span', attrs={'class': 'rating'})
        hotel.guest_rating = gr.text

        # Address
        add = soup.find('span', attrs={'class':'property-address'})
        hotel.address = add.text

        # ZIP
        hotel.zip_code = add.find('span', attrs={"class": 'postal-code'}).text.replace(',', '')

        # desc
        hotel.desc = soup.find('div', attrs={'class': 'tagline'}).text

        # Wifi and breakfast
        wifi = soup.find('span',attrs={'class': 'freebie item'}).text
        if "wifi" in wifi.lower():
            hotel.wifi = 1
        if "breakfast" in wifi.lower():
            hotel.breakfast = 1

        # swimming pool
        pool = soup.find('div',attrs={'id': 'overview'}).text
        if "pool" in pool.lower():
            hotel.swimming_pool = 1

        # Capacity
        cap = soup.find('div',attrs={'id': 'overview-section-4'})
        cap = cap.find('li').text
        hotel.capacity = re.findall("\d+", cap)[0]

        return hotel
    except:
        pass


def scrape_url(url):
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    firefox_capabilities['binary'] = '\\usr\\local\\bin'
    driver = webdriver.Firefox(capabilities=firefox_capabilities)


    # Load WebDriver and navigate to the page url.
    # This will open a browser window.
    driver.get(url)

    urls = []

    # First scroll to the end of the table by sending Page Down keypresses to
    # the browser window.
    for i in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    # Once the whole table has loaded, grab all the visible links.
    html_source = driver.page_source
    driver.quit()
    return html_source


searches = [(str(date).split(' ')[0], get_search_url(str(date).split(' ')[0])) for date in dates]

hotels = []

for search in searches:
    html = bs(scrape_url(search[1]), 'html.parser')

    links = [str("https://www.hotels.com/" + td.find('a',attrs={'target':'_blank'})['href']) for td in html.findAll('h3', attrs={'class':'p-name'})]
    links = [link for link in links if "travelads" not in link]
    try:
        for link in links:
            a = get_hotel_details(link, search[0])
            if a is not None:
                hotels.append(a)
    except:
        print("Error")
    print(len(hotels), len(links))
    # break

# print([x.name for x in hotels])

hotels = sorted(hotels, key=lambda x: x.name)
# print()
# print([x.name for x in hotels])

hot_names = [x.name for x in hotels]
hot_names = set(hot_names)

for n in hot_names:
    hot_count = [p for p in hotels if p.name == n]
    if len(hot_count) < 10:
        hotels.extend([hot_count[0]]*(10 - len(hot_count)))
# print()
# print([x.name for x in hotels])
hotels = sorted(hotels, key=lambda x: x.name)
# print()
# print([x.name for x in hotels])
print(len(hotels))
output = [str(h.get_csv() + "\n") for h in hotels if h is not None]

with open('output.csv', 'w') as f:
    f.writelines(output)
