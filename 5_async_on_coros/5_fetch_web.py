from time import time

import requests
import aiohttp
import asyncio

URL = "https://api.thecatapi.com/v1/images/search"
TOTAL_REQUESTS = 10


def do_sync_requests(url):
    t0 = time()
    for _ in range(TOTAL_REQUESTS):
        resp = requests.get(url)
        print(resp.json()[0].get("url"))
    t1 = time()

    print(f"Sync total time: {t1 - t0}")


async def aio_fetch_url(url):
    t0 = time()

    async with aiohttp.ClientSession() as session:
        for _ in range(TOTAL_REQUESTS):
            async with session.get(url) as response:
                data = await response.json()
                print(data[0].get("url"))
    t1 = time()
    print(f"Async total time: {t1 - t0}")


if __name__ == '__main__':
    do_sync_requests(URL)
    print("=" * 100)
    asyncio.run(aio_fetch_url(URL))
    print("=" * 100)
