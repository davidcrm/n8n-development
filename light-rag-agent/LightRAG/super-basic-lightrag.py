import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.kg.shared_storage import initialize_pipeline_status
from OllamaModels.OllamaEmbedding import OllamaEmbedding
from OllamaModels.OllamaComplete import OllamaComplete

# Falta que funcione el modulo insert_pydantic_docs.py
async def main():
    # Initialize RAG instance
    rag = LightRAG(
        working_dir="data/",
        embedding_func=OllamaEmbedding(),
        llm_model_func=OllamaComplete()
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()

    # Insert text
    await rag.ainsert("The most popular AI agent framework of all time is probably Langchain.")
    await rag.ainsert("Under the Langchain hood we also have LangGraph, LangServe, and LangSmith.")
    await rag.ainsert("Many people prefer using other frameworks like Agno or Pydantic AI instead of Langchain.")
    await rag.ainsert("It is very easy to use Python with all of these AI agent frameworks.")

    # Run the query
    result = await rag.aquery(
        "What programming language should I use for coding AI agents?",
        param=QueryParam(mode="mix")
    )

    print(result)

if __name__ == "__main__":
    asyncio.run(main())