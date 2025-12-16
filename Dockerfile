FROM python:3.10-slim

# --------------------------------------
# System dependencies (for Whisper)
# --------------------------------------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------
# Set working directory
# --------------------------------------
WORKDIR /app

# --------------------------------------
# Copy dependency file first (cache)
# --------------------------------------
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# --------------------------------------
# Copy application code
# --------------------------------------
COPY . .

# --------------------------------------
# Expose Hugging Face default port
# --------------------------------------
EXPOSE 7860

# --------------------------------------
# Start FastAPI app
# --------------------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
