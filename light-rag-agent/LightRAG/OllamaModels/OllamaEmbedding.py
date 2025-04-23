import httpx

# Clase para instanciar el modelo de embeddings de ollama con un metodo que se llama al instanciarse la clase que recibe el modelo que va a trabajar y el prompt
class OllamaEmbedding:
    def __init__(self, model: str = "nomic-embed-text:latest"):
        self.model = model
        self.embedding_dim = 768

    async def __call__(self, input: str) -> list:
        url = "http://localhost:11434/api/embed"
        payload = {
            "model": self.model,
            "input": input
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()["embeddings"]
