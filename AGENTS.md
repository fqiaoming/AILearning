# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

This is an AI course repository (AI大模型应用开发 - 从入门到精通) containing markdown lessons and Python example scripts. There is no traditional web application or backend service — the runnable code consists of standalone Python scripts in `ai_learning/` and `ai-course-code/`.

### Python Environment

- **Python 3.12** is required (3.10–3.12 supported; 3.13+ is incompatible with LangChain v1.x).
- Virtual environment lives at `ai_learning/.venv`. Activate with `source /workspace/ai_learning/.venv/bin/activate`.
- `python3.12-venv` system package must be installed for venv creation.

### Running Tests

- `python ai_learning/test_all.py` — checks all dependency imports + LM Studio API + LangChain invocation.
- `python ai-course-code/chapter02_environment/test_env.py` — basic environment validation. Note: the `python-dotenv` check shows ❌ due to a package-name-to-module-name mapping issue in the script (`python_dotenv` vs `dotenv`); the package is actually installed and works.

### LLM Server Requirement

All example scripts expect an OpenAI-compatible API at `http://localhost:1234/v1` (default LM Studio endpoint). In cloud environments without LM Studio, you can run a mock server to satisfy the API calls. See `/tmp/mock_llm_server.py` for an example using FastAPI + uvicorn on port 1234.

### Key Dependencies

Installed via pip into the venv: `langchain`, `langchain-openai`, `langchain-community`, `chromadb`, `tiktoken`, `python-dotenv`, `openai`, `requests`, `fastapi`, `uvicorn`.

### Lint / Build

This is a documentation + script repository — there is no formal linter, build system, or CI pipeline configured.
