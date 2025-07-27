FROM python:3.9-slim

# Install system-level dependencies including tesseract-ocr
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Render uses PORT env var automatically)
EXPOSE 10000

# Start app with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
