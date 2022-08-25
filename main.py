import asyncio

from mongoengine import connect

from constants import OLX_BASE_URL
from services.olx_scraper import olx_scraper_service

# connect to mongoDB
connect('gloves-db')

html = olx_scraper_service.get_page_html(f"{OLX_BASE_URL}/d/uk/hobbi-otdyh-i-sport/q-Перчатки для бокса")
links = olx_scraper_service.find_olx_links(html)

asyncio.run(olx_scraper_service.get_all_links_data(links))
