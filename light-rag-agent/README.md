# LightRAG vs BasicRAG: Comparing RAG Implementations

This project demonstrates two different implementations of Retrieval-Augmented Generation (RAG) for answering questions about Pydantic AI using its documentation:

1. **BasicRAG**: A traditional RAG implementation using ChromaDB for vector storage and similarity search
2. **LightRAG**: An advanced, lightweight RAG implementation with enhanced knowledge graph capabilities

## Project Goal

The primary goal of this project is to showcase the power and efficiency of LightRAG compared to traditional RAG implementations. LightRAG offers several advantages:

- **Simplified API**: LightRAG provides a more streamlined API with fewer configuration parameters
- **Automatic Document Processing**: LightRAG handles document chunking and embedding automatically
- **Knowledge Graph Integration**: LightRAG leverages knowledge graph capabilities for improved context understanding
- **More Efficient Retrieval**: LightRAG's query mechanism provides more relevant results with less configuration

## Installation

### Prerequisites
- Python 3.11+
- OpenAI API key

### Setup

1. Clone this repository

2. Create a `.env` file in both the `BasicRAG` and `LightRAG` directories (or whichever you want to use) with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Set up a virtual environment and install dependencies:

   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   
   # Install dependencies for LightRAG
   cd LightRAG
   pip install -r requirements.txt
   
   # In a new terminal with activated venv, install BasicRAG dependencies
   cd BasicRAG
   pip install -r requirements.txt
   ```

## Running the Implementations

### LightRAG (Most Powerful)

1. **Insert Documentation** (this will take a while - using full Pydantic AI docs as an example!):
   ```bash
   cd LightRAG
   python insert_pydantic_docs.py
   ```
   This will fetch the Pydantic AI documentation and process it using LightRAG's advanced document processing.

2. **Run the Agent**:
   ```bash
   python rag_agent.py --question "How do I create a Pydantic AI agent?"
   ```

3. **Run the Interactive Streamlit App**:
   ```bash
   streamlit run streamlit_app.py
   ```
   This provides a chat interface where you can ask questions about Pydantic AI.

### BasicRAG

1. **Insert Documentation** (this will take a while - using full Pydantic AI docs as an example!):
   ```bash
   cd BasicRAG
   python insert_pydantic_docs.py
   ```
   This will fetch and process the Pydantic AI documentation into ChromaDB with manual chunking.

2. **Run the Agent**:
   ```bash
   python rag_agent.py --question "How do I create a Pydantic AI agent?"
   ```
   You can customize the number of results from the vector DB with `--n-results 10`.

3. **Run the Interactive Streamlit App**:
   ```bash
   streamlit run streamlit_app.py
   ```

## Key Differences Between Implementations

### Document Processing
- **BasicRAG**: Manually splits documents into chunks with specified size and overlap, requiring careful tuning
- **LightRAG**: Automatically handles document processing with intelligent chunking

### Vector Storage
- **BasicRAG**: Uses ChromaDB directly with manual collection management
- **LightRAG**: Abstracts storage details behind a clean API with optimized defaults

### Query Mechanism
- **BasicRAG**: Requires specifying the number of results to return
- **LightRAG**: Uses a more sophisticated query mechanism with different modes (e.g., "naive" or "hybrid")

### Code Complexity
- **BasicRAG**: Requires more boilerplate code for setting up collections and processing documents
- **LightRAG**: Offers a more concise API with fewer lines of code needed

## Project Structure

### LightRAG
- `LightRAG/rag_agent.py`: Pydantic AI agent using LightRAG
- `LightRAG/insert_pydantic_docs.py`: Script to fetch and process documentation
- `LightRAG/streamlit_app.py`: Interactive web interface

### BasicRAG
- `BasicRAG/rag_agent.py`: Pydantic AI agent using traditional RAG with ChromaDB
- `BasicRAG/insert_pydantic_docs.py`: Script for document processing with manual chunking
- `BasicRAG/utils.py`: Utility functions for ChromaDB operations
- `BasicRAG/streamlit_app.py`: Interactive web interface

## Comparing Performance

To compare the performance of both implementations:

1. Run both Streamlit apps (in separate terminals)
2. Ask the same questions to both agents
3. Compare the quality and relevance of responses
4. Note the differences in response time and accuracy

LightRAG typically provides more contextually relevant answers with less configuration, demonstrating the advantages of its enhanced knowledge graph capabilities and optimized retrieval mechanisms.
