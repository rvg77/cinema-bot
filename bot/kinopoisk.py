import aiohttp
from urllib.parse import quote
import typing as tp


async def film2info(film: str) -> tp.Dict[str, tp.Any]:
    film_encoded = quote(film)
    url = f"http://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={film_encoded}&page=1"
    headers = {'accept': 'application/json', 'X-API-KEY': 'f8565f16-e10a-49b1-a260-b3a6dc819f57'}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            json_body = await r.json()
            return json_body
