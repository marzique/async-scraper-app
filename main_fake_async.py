import asyncio
import timeit

from mongoengine import connect

from constants import OLX_BASE_URL
from services.olx_scraper_fake_async import olx_scraper_fake_async_service

# connect to mongoDB

connect('gloves-db')

html = asyncio.run(olx_scraper_fake_async_service.get_page_html(f"{OLX_BASE_URL}/d/uk/hobbi-otdyh-i-sport/q-Перчатки для бокса"))
links = asyncio.run(olx_scraper_fake_async_service.find_olx_links(html))


start = timeit.default_timer()

asyncio.run(olx_scraper_fake_async_service.get_all_links_data(links))

execution_time = timeit.default_timer() - start
print("Program Executed in " + str(execution_time))
