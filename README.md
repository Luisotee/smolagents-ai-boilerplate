# AI Assistant Service

This is an AI Assistant service built with FastAPI and SmolagentS. It provides a flexible and extensible backend for AI-powered chat applications with various client integrations.

## Features

- 🤖 Powered by Azure OpenAI GPT-4o-mini
- 🔄 Persistent conversation history with Supabase
- 📎 File attachment support
- 🌐 Platform-agnostic messaging format
- 🛠️ Extensible tool system
- 🔒 Environment-based configuration

## Prerequisites

- Python 3.10 or higher
- Poetry package manager
- Supabase instance (local or cloud)
- Azure OpenAI API access

## Setup

1. Install Poetry if you don't have it already:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone the repository and navigate to the AI module:

   ```bash
   cd ai
   ```

3. Copy the environment file and configure your variables:

   ```bash
   cp .env.example .env
   ```

4. Install dependencies:
   ```bash
   poetry install
   ```

## Running the Service

### Development Mode

```bash
poetry run uvicorn ai_assistant.main:app --reload --host 0.0.0.0 --port 40000
```

### Production Mode

```bash
poetry run start
```

## API Documentation

Once running, access the API documentation at:

- Swagger UI: `http://localhost:40000/docs`

## Project Structure

```
src/ai_assistant/
├── agents/         # AI agent definitions and tools
├── api/            # FastAPI routes and endpoints
├── config/         # Configuration and settings
├── database/       # Database connections and models
├── prompts/        # System prompts and templates
└── utils/          # Utility functions and helpers
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
