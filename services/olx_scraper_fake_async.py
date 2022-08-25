import asyncio
import random

import requests
from bs4 import BeautifulSoup

from constants import OLX_BASE_URL


class OLXFakeSyncScraperService:
    @staticmethod
    async def get_page_html(url):
        response = requests.get(url)
        return response.text

    @staticmethod
    async def find_olx_links(html):
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.find_all("div", attrs={"data-cy": "l-card"})

        links = []
        for row in cards:
            if not row.find("div", attrs={"data-testid": "adCard-featured"}):
                if link := row.find("a").get("href"):
                    full_link = f"{OLX_BASE_URL}{link}"
                    links.append(full_link)
        return links

    async def get_all_links_data(self, urls):
        all_data = await asyncio.gather(*(self.scrape_glove_page(url) for url in urls))
        print(all_data)

    async def scrape_glove_page(self, url) -> dict:
        print(f"Scraping url: {url}")
        html = await self.get_page_html(url)
        soup = BeautifulSoup(html, "html.parser")

        glove_data = {
            "full_name": soup.find("h1", attrs={"data-cy": "ad_title"}).get_text(),
            # "price": self._get_price(soup),
            # "size": self._get_size(soup),
            # "description": self._get_description(soup),
            "olx_url": url,
        }
        print(f"Scraped url: {url}")
        return glove_data

    @staticmethod
    def _get_price(soup: BeautifulSoup) -> int:
        tag = soup.find("h3", attrs={"data-testid": "ad-price-container"})
        print(tag)
        price = int(tag.get_text().split(" ")[0])
        return price

    @staticmethod
    def _get_size(soup: BeautifulSoup) -> int:
        # TODO:
        return random.choice([12, 14, 16])

    @staticmethod
    def _get_description(soup: BeautifulSoup) -> str:
        tag = soup.find("h3", attrs={"data-cy": "ad_description"})
        description = tag.find("div").get_text()
        return description


olx_scraper_fake_async_service = OLXFakeSyncScraperService()
