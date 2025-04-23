import os
import argparse
from dataclasses import dataclass
import asyncio
from pydantic_ai import RunContext
from pydantic_ai.agent import Agent
from OllamaModels.OllamaComplete import OllamaComplete
from OllamaModels.OllamaEmbedding import OllamaEmbedding
from lightrag import LightRAG, QueryParam
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Directorio donde se supone que carga los datos
# Mejor si se carga en una base de datos o donde sea
WORKING_DIR = "./vector-docs"

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=OllamaEmbedding(),
        llm_model_func=OllamaComplete()
    )

    await rag.initialize_storages()

    return rag


@dataclass
class RAGDeps:
    """Dependencies for the RAG agent."""
    lightrag: LightRAG

ollama_model = OpenAIModel(
    model_name='mistral', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)

# Create the Pydantic AI agent
agent = Agent(
    ollama_model,
    deps_type=RAGDeps,
    system_prompt="You are a helpful assistant that answers questions about an AI company based on the provided documentation. "
                  "Use the retrieve tool to get relevant information from the documentation before answering. "
                  "If the documentation doesn't contain the answer, clearly state that the information isn't available "
                  "in the current documentation and provide your best general knowledge response."
)


@agent.tool
async def retrieve(context: RunContext[RAGDeps], search_query: str) -> str:
    print(f"🛠️ Retrieve ha sido invocado con la query: {search_query}")
    result = await context.deps.lightrag.aquery(
        search_query, param=QueryParam(mode="global")
    )
    print("📄 Resultado del retrieve:", result)
    return result


async def run_rag_agent(question: str,) -> str:
    """Run the RAG agent to answer a question about Pydantic AI.
    
    Args:
        question: The question to answer.
        
    Returns:
        The agent's response.
    """
    # Create dependencies
    lightrag = await initialize_rag()
    deps = RAGDeps(lightrag=lightrag)
    
    # Run the agent
    result = await agent.run(question, deps=deps)
    
    return result.data


def main():
    """Main function to parse arguments and run the RAG agent."""
    parser = argparse.ArgumentParser(description="Run an AI agent with RAG using ChromaDB")
    parser.add_argument("--question", help="The question to answer about IA Solutions Corp")
    
    args = parser.parse_args()
    
    # Run the agent
    response = asyncio.run(run_rag_agent(args.question))
    
    print("\nResponse:")
    print(response)


if __name__ == "__main__":
    main()
