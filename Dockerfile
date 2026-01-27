FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY gmail_puller.py .

# Create volume mount point for credentials
VOLUME ["/app/config"]

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "gmail_puller.py"]
