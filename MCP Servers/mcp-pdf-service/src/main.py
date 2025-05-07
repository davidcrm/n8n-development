from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
from utils import PdfService
import asyncio

import os


load_dotenv()

# Contexto vacío (Extendible si necesario)
@dataclass
class AppContext:
    pass

# Gestiona el ciclo de vida del servidor
@asynccontextmanager
async def app_lifespan(server:FastMCP) -> AsyncIterator[AppContext]:
    yield AppContext()

# Inicializar el servidor MCP con el contexto vacío que hemos creado
mcp = FastMCP(
    "mcp-pdf-service",
    description="MCP server for generating pdf files with info asked",
    lifespan= app_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=os.getenv("PORT", "8070")
)        

@mcp.tool()
async def generar_pdf(ctx:Context, content: str, title: str = "Report") -> str:
    try: 
        filepath = PdfService.generate_pdf(content, title)

        return f"PDF generado correctamente en la ruta: {filepath}"
    except Exception as e:
        return f"Error generando el PDF: {str(e)}"

async def main():
    transport = os.getenv("TRANSPORT", "sse")
    if transport == 'sse':
        # Run the MCP server with sse transport
        await mcp.run_sse_async()
    else:
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())
