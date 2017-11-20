This program scrapes hotels.com for hotels in given city. 

You only need to provide a search url for city and occupany. 

You can have a list of dates over which searches are made automatically using the url above and data is scraped.

Data is scraped according to following file:
https://docs.google.com/document/d/1LujatvJQ5eqA0NXRHEkulkhOCjKEUMO-O0djw0iOQDY

Done as a project for a MBA program in one of the most prestigious MBA schools in India.

Scraping is done using BeautifulSoup.

hotels.com has infinite scroll search page with only 10 results showing at one time. 
I have used Selenium to emulate scrolling using FireFox driver.

You will need geckodriver binary for FireFox driver to work. download appropriate geckodriver and place it in /usr/local/bin. Or download it and add the folder to PATH variable.

Still needs fine tuning, sometimes the hotel's link navigate to search page itself. But gets around 400-450 results with various details about each hotel, such as max rent, actual rent, free wifi, free breakfast and swimming pool. Still to add Availability on a date feature, since the website just does not show search results if hotels are not available on a date.