from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
from utils import ApiService
import asyncio
import os

load_dotenv()

# Contexto vacío
@dataclass
class AppContext:
    pass

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    yield AppContext()

# Inicializar el servidor MCP
mcp = FastMCP(
    "mcp-api-service",
    description="MCP server for querying external APIs and returning data",
    lifespan=app_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=os.getenv("PORT", "8080")
)

@mcp.tool()
async def consultar_api(ctx: Context, url: str) -> str:
    """
    Consulta un endpoint de una API externa y devuelve el contenido como texto.
    """
    try:
        data = await ApiService.fetch_data(url)
        return f"Respuesta de la API:\n{data}"
    except Exception as e:
        return f"Error al consultar la API: {str(e)}"

async def main():
    transport = os.getenv("TRANSPORT", "sse")
    if transport == "sse":
        await mcp.run_sse_async()
    else:
        await mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())
