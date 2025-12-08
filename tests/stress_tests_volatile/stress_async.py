import asyncio
import aiohttp
import sys

URL = sys.argv[1]

CONNECTIONS = 10000

async def hit(session, i):
    try:
        async with session.get(URL) as resp:
            await resp.text()
    except Exception as e:
        print(f"Request {i} failed:", e)

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [hit(session, i) for i in range(CONNECTIONS)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())