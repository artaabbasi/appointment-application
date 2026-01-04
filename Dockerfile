FROM python:3.14

# Install system dependencies and tools
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    ca-certificates \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.2.1

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Set working directory and copy dependency files
WORKDIR /fastapi
COPY poetry.lock pyproject.toml ./

# Install Python dependencies without creating virtualenv
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

# Copy the application code
COPY src .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
