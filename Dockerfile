FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY pyproject.toml .
COPY LICENSE .
COPY README.md .
RUN pip install --no-cache-dir .

# Copy source
COPY src/ src/

# Re-install in editable mode so the entry point is registered
RUN pip install --no-cache-dir -e .

# Azure Container Apps injects PORT; default to 8000
ENV PORT=8000
ENV HOST=0.0.0.0
ENV MCP_TRANSPORT=sse
# No TEAMVIEWER_API_TOKEN here — each user supplies their own token via /sse?token=

EXPOSE 8000

CMD ["mcp-teamviewer"]
