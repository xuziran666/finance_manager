FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --no-dev

COPY . .

CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
