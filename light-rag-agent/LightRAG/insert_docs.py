import os
import asyncio
from lightrag import LightRAG
from lightrag.kg.shared_storage import initialize_pipeline_status
from OllamaModels.OllamaComplete import OllamaComplete
from OllamaModels.OllamaEmbedding import OllamaEmbedding
import fitz

FILES_DIR = "./docs"
WORKING_DIR = "./vector-docs"

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# pip install pymupdf
def read_pdf(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text
    
# Función para leer los archivos de texto de una carpeta y devolver su contenido
def leer_documentos_locales(carpeta:str) -> list[str]:
    documentos = []
    
    for file in os.listdir(carpeta):
        path = os.path.join(carpeta,file)
        if file.endswith(".txt") or file.endswith(".md"):
            with open(path, "r",encoding="utf-8") as f:
                documentos.append(f.read())
        elif file.endswith(".pdf"):
            documentos.append(read_pdf(path))
    print(f"La lista tiene {len(documentos)} documentos")
    return documentos

async def initialize_rag():
    # Create RAG instance
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func = OllamaEmbedding(),
        llm_model_func = OllamaComplete(),
    )

    # Initialize storage and pipeline status
    await rag.initialize_storages()
    await initialize_pipeline_status()

    # Return the instance
    return rag


async def main():
    docs = leer_documentos_locales(FILES_DIR)
    rag = await initialize_rag()

    if not docs:
            print("⚠️ No se encontraron documentos en la carpeta ./docs.")
            return
    
    for idx, doc in enumerate(docs):
        print(f"📄 Insertando documento {idx + 1} (longitud: {len(doc)} caracteres)")
        await rag.ainsert(doc) # Para insertar documentos, entidades y relaciones # No funciona por el modelo de Ollama
        

if __name__ == "__main__":
    asyncio.run(main())
