import asyncio
import random

import aiohttp
from bs4 import BeautifulSoup

from constants import OLX_BASE_URL


class OLXTrueSyncScraperService:
    last_page = None
    current_url = None
    links = []

    @staticmethod
    async def get_page_html(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get_all_links(self, url):
        async def get_page_links(page):
            self.current_url = f"{url}?page={page}"
            html = await self.get_page_html(session, url)
            page_links = await self.find_olx_links(html)
            return page_links

        async with aiohttp.ClientSession() as session:
            starting_html = await self.get_page_html(session, url)
            if not self.last_page:
                self.last_page = self._find_last_page(starting_html)
            coroutines = [get_page_links(i) for i in range(self.last_page)]
            return await asyncio.gather(*coroutines)

    @staticmethod
    def _find_last_page(html):
        soup = BeautifulSoup(html, "html.parser")
        pagination_list = soup.find("ul", attrs={"data-testid": "pagination-list"})
        last = pagination_list.find_all("li")[-1].get_text()
        return int(last)

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

    async def get_all_links_data(self, url_batches):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for urls in url_batches:
                for url in urls:
                    task = asyncio.create_task(self.scrape_glove_page(session, url))
                    tasks.append(task)
                results = await asyncio.gather(*tasks)
                print(results)

    async def scrape_glove_page(self, session, url) -> dict:
        print(f"Scraping url: {url}")
        html = await self.get_page_html(session, url)
        soup = BeautifulSoup(html, "html.parser")

        glove_data = {
            "full_name": soup.find("h1", attrs={"data-cy": "ad_title"}).get_text(),
            "price": self._get_price(soup),
            "size": self._get_size(soup),
            "description": self._get_description(soup),
            "olx_url": url,
        }
        print(f"Scraped url: {url}")
        return glove_data

    @staticmethod
    def _get_price(soup: BeautifulSoup) -> int:
        tag = soup.find("div", attrs={"data-testid": "ad-price-container"})
        price = int(tag.get_text().split(" ")[0])
        return price

    @staticmethod
    def _get_size(soup: BeautifulSoup) -> int:
        # TODO:
        return random.choice([12, 14, 16])

    @staticmethod
    def _get_description(soup: BeautifulSoup) -> str:
        tag = soup.find("div", attrs={"data-cy": "ad_description"})
        description = tag.find("div").get_text()
        return description


olx_scraper_true_async_service = OLXTrueSyncScraperService()
