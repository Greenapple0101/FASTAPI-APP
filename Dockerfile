FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure directories exist and set permissions
RUN mkdir -p templates && \
    chmod -R 755 /app && \
    chmod 666 todo.json 2>/dev/null || touch todo.json && chmod 666 todo.json

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

