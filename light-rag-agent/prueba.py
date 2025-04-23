import asyncio
from OllamaModels.OllamaEmbedding import OllamaEmbedding

async def test_embedding():
    embed = OllamaEmbedding("nomic-embed-text")
    result = await embed("Texto de prueba")
    print(f"Dimensiones del vector: {len(result[0])}")

asyncio.run(test_embedding())
