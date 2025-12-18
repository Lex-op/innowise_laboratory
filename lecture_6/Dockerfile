# Python base image
FROM python:3.11-slim

# Create non-privileged user for security
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code with correct ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8000

# Entrypoint with fixed command
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0"]

# Default runtime arguments
CMD ["--port", "8000"]