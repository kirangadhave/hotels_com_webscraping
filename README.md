This program scrapes hotels.com for hotels in given city. 

You only need to provide a search url for city and occupany. 

You can have a list of dates over which searches are made automatically using the url above and data is scraped.

Data is scraped according to following file:
https://docs.google.com/document/d/1LujatvJQ5eqA0NXRHEkulkhOCjKEUMO-O0djw0iOQDY/edit?usp=sharing

Done as a project for a MBA program in one of the most prestigious MBA schools in India.

Scraping is done using BeautifulSoup.

hotels.com has infinite scroll search page with only 10 results showing at one time. 
I have used Selenium to emulate scrolling using FireFox driver.

You will need geckodriver binary for FireFox driver to work. download appropriate geckodriver and place it in /usr/local/bin. Or download it and add the folder to PATH variable.

Still needs fine tuning, sometimes the hotel's link navigate to search page itself. But gets around 400-450 results with various details about each hotel, such as max rent, actual rent, free wifi, free breakfast and swimming pool. Still to add Availability on a date feature, since the website just does not show search results if hotels are not available on a date.


Run following steps:
1. Check if python3.6 installed
2. Check if pip3 is installed
3. Download BeautifulSoup
    pip3 install BeautifulSoup4

4. Download geckodriver for appropriate version from here:
    https://github.com/mozilla/geckodriver/releases

5. Unzip the archive and move the binary to /usr/local/bin. (may require root access)
6. Will also need FireFox to be installed.

To use:
Go to hotels.com and make a search for a city with occupancy settings as desired. Copy the URL of search results. It looks as follows:

    https://www.hotels.com/search.do?resolved-location=CITY%3A1489699%3AUNKNOWN%3AUNKNOWN&destination-id=1489699&q-destination=Asheville,%20North%20Carolina,%20United%20States%20of%20America&q-check-in=2017-11-29&q-check-out=2017-12-07&q-rooms=1&q-room-0-adults=2&q-room-0-children=0
In the long url above there is a term which looks like: "check-in=2017-11-29&q-ch"

We will split the above url in 3 parts. Before the date, date and after the date. We can then replace our date string with the date we want. This is what the get_search_url method does.