# api/Dockerfile

ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint script:
# launch the application and create the database
ENTRYPOINT ["/app/entrypoint.sh"]
