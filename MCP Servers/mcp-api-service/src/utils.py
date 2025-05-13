import httpx
import os

class ApiService:
    # Debe ser la url del .env y si no la hay pues por defecto pone esa
    BASE_URL = os.getenv("BASE_URL","https://catfact.ninja/")


    @staticmethod
    def build_url(endpoint: str) -> str:
        """
            Construye la URL completa concatenando la base y el endpoint.
        """
        # Asegurarse de que hay exactamente una sola '/' entre base y endpoint
        if not ApiService.BASE_URL.endswith("/"):
            base = ApiService.BASE_URL + "/"
        else:
            base = ApiService.BASE_URL

        endpoint = endpoint.lstrip("/")  # quitar '/' inicial si lo tiene
        return base + endpoint


    @staticmethod
    async def fetch_data(url: str) -> str:
        """
        Hace una petición HTTP GET al endpoint especificado y devuelve el contenido como texto.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        