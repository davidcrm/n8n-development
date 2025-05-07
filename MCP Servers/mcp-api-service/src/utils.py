import httpx

class ApiService:
    @staticmethod
    async def fetch_data(url: str) -> str:
        """
        Hace una petición HTTP GET al endpoint especificado y devuelve el contenido como texto.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
