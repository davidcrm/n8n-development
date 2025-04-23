import httpx


# Clase para instanciar el modelo generativo de ollama con un metodo que se llama al instanciarse la clase que recibe el modelo que va a trabajar y el prompt
class OllamaComplete:
    def __init__(self, model: str = "qwen2.5:7b-instruct-q4_K_M"):
        self.model = model

    # Puede aceptar parámetros inesperados
    async def __call__(self, prompt: str, **kwargs) -> str:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()["response"]
