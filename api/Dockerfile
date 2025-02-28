ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}

ENV API_PORT=8000

# Set working directory
WORKDIR /app

# Copy requirements first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose FastAPI port
EXPOSE ${API_PORT}

# Start FastAPI using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
