# Reproducible deployment definition for the Level 3 multi-tool agent.
# Build:  docker build -t ai-agent-level3 .
# Run:    docker run -p 8080:8080 -e GEMINI_API_KEY=your_key_here ai-agent-level3
# Test:   curl -X POST http://localhost:8080/ask -H "Content-Type: application/json" \
#           -d '{"question": "What is the weather in Dubai?"}'

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agent.py weather_tool.py currency_tool.py app.py ./

# GEMINI_API_KEY must be injected at run time (docker run -e, or the
# hosting platform's secret manager) - never baked into the image.
ENV PORT=8080
EXPOSE 8080

CMD ["python3", "app.py"]