import httpx


class ArtInstituteAPI:
    BASE_URL = "https://api.artic.edu/api/v1"

    @classmethod
    async def get_artwork(cls, artwork_id: int) -> dict | None:
        """Fetch artwork from Art Institute Chicago API by external ID."""
        url = f"{cls.BASE_URL}/artworks/{artwork_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                return None
            data = response.json().get("data")
            if not data:
                return None
            return {
                "external_id": data.get("id"),
                "title": data.get("title"),
                "artist_title": data.get("artist_title"),
                "image_id": data.get("image_id"),
            }

    @classmethod
    async def search_artworks(cls, query: str, page: int = 1, limit: int = 10) -> list[dict]:
        """Search artworks in Art Institute Chicago API."""
        url = f"{cls.BASE_URL}/artworks/search"
        params = {"q": query, "page": page, "limit": limit}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code != 200:
                return []
            data = response.json().get("data", [])
            return [
                {
                    "external_id": item.get("id"),
                    "title": item.get("title"),
                    "artist_title": item.get("artist_title"),
                    "image_id": item.get("image_id"),
                }
                for item in data
            ]