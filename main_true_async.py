import asyncio
import timeit

from mongoengine import connect

from constants import OLX_BASE_URL
from services.olx_scraper_true_async import olx_scraper_true_async_service


# connect to mongoDB
connect('gloves-db')


start = timeit.default_timer()

links = asyncio.run(olx_scraper_true_async_service.get_all_links(f"{OLX_BASE_URL}/d/uk/hobbi-otdyh-i-sport/q-Перчатки для бокса/"))
asyncio.run(olx_scraper_true_async_service.get_all_links_data(links))

execution_time = timeit.default_timer() - start
print("Program Executed in " + str(execution_time))

print(olx_scraper_true_async_service.data)
