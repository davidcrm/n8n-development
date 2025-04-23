<h1 align="center">MCP-TextParser: Text Structure Analyzer for AI Agents</h1>

<p align="center">
  <img src="public/Mem0AndMCP.png" alt="Mem0 and MCP Integration" width="600">
</p>

A template implementation of the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that extracts titles and subtitles from any text input, demonstrating modular tool creation.

Use this as a reference to build your own MCP tools for AI agents that need to analyze or parse structured text.

## Overview

This project demonstrates how to build an MCP server that enables AI agents to parse and extract structured data from text documents. It serves as a practical example of creating your own MCP servers for various natural language processing tasks.

The implementation follows best practices for modular, clean MCP server design, allowing seamless integration with any MCP-compatible client.

## Features

The server provides one primary tool:

1. **`analyze_text_structure`**: Parses input text and returns a structured JSON with detected titles and subtitles.

## Prerequisites

- Python 3.12+
- Docker if running the MCP server as a container (recommended)

## Installation

### Using uv

1. Install uv if you don't have it:
   ```bash
   pip install uv
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/mcp-text-parser.git
   cd mcp-text-parser
   ```

3. Install dependencies:
   ```bash
   uv pip install -e .
   ```

4. Create a `.env` file (optional, only needed for custom configuration)

### Using Docker (Recommended)

1. Build the Docker image:
   ```bash
   docker build -t mcp/text-parser --build-arg PORT=8060 .
   ```

## Configuration (Optional)

| Variable | Description | Example |
|----------|-------------|----------|
| `TRANSPORT` | Transport protocol (sse or stdio) | `sse` |
| `HOST` | Host to bind to when using SSE transport | `0.0.0.0` |
| `PORT` | Port to listen on when using SSE transport | `8060` |

## Running the Server

### Using uv

#### SSE Transport

```bash
# Set TRANSPORT=sse in .env then:
uv run src/main.py
```

#### Stdio Transport

```bash
# Set TRANSPORT=stdio in .env then:
uv run src/main.py
```

### Using Docker

#### SSE Transport

```bash
docker run --env-file .env -p 8060:8060 mcp/text-parser
```

## Integration with MCP Clients

### SSE Configuration

```json
{
  "mcpServers": {
    "textParser": {
      "transport": "sse",
      "url": "http://localhost:8060/sse"
    }
  }
}
```

### Stdio Configuration

```json
{
  "mcpServers": {
    "textParser": {
      "command": "your/path/to/venv/python",
      "args": ["your/path/to/src/main.py"],
      "env": {
        "TRANSPORT": "stdio"
      }
    }
  }
}
```

## Building Your Own Server

This template provides a foundation for creating new MCP microservices:

1. Add tools with the `@mcp.tool()` decorator
2. Create a custom context and lifespan function if needed
3. Abstract logic into `utils.py` for reusability and testability
4. Use `@mcp.prompt()` and `@mcp.resource()` as needed to enrich your tools

---

