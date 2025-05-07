from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
import asyncio
import os

from utils import extract_titles

# Carga las variables definidas en el archivo .env (como HOST y PORT)
load_dotenv()

# Creamos un dataclass para el contexto de este microservicio MCP.
# En este caso no necesita ninguna inicialización, pero se deja la estructura por consistencia y posible expansión.
@dataclass
class AnalyzerContext:
    """Contexto del servidor MCP para análisis de texto."""
    pass

# Función de ciclo de vida del servidor (lifespan).
# Aquí podrías inicializar conexiones, cargar modelos, etc. De momento no hace falta.
@asynccontextmanager
async def analyzer_lifespan(server: FastMCP) -> AsyncIterator[AnalyzerContext]:
    yield AnalyzerContext()

# Creamos el servidor FastMCP con nombre, descripción, contexto, host y puerto
mcp = FastMCP(
    "mcp-text-analyzer",  # Nombre del microservicio
    description="Servidor MCP para extraer títulos y subtítulos de texto",
    lifespan=analyzer_lifespan,  # Función de contexto
    host=os.getenv("HOST", "0.0.0.0"),  # IP (por defecto acepta conexiones externas)
    port=os.getenv("PORT", "8060")  # Puerto configurable (por defecto 8060)
)

# Definimos una herramienta del servidor MCP: get_titles
# Esta función recibe un texto y devuelve los títulos/subtítulos encontrados
@mcp.tool()
async def get_titles(ctx: Context, text: str) -> list[str]:
    """
    Extrae títulos y subtítulos de un texto.

    Args:
        ctx: Contexto del servidor MCP (no se utiliza en esta herramienta).
        text: Texto del documento a analizar.

    Returns:
        Lista de líneas que representan títulos o subtítulos del documento.
    """
    try:
        titles = extract_titles(text)  # Se usa la función del módulo utils
        return titles if titles else ["No se encontraron títulos."]
    except Exception as e:
        return [f"Error al analizar el texto: {str(e)}"]

# Función principal que decide si lanzar el servidor en modo SSE (eventos) o STDIO
async def main():
    transport = os.getenv("TRANSPORT", "sse")
    if transport == "sse":
        await mcp.run_sse_async()  # Modo recomendado para servidores web
    else:
        await mcp.run_stdio_async()  # Modo útil para pruebas por consola

# Ejecutamos la función main si se ejecuta directamente el script
if __name__ == "__main__":
    asyncio.run(main())