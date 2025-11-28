FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps for numpy, scipy, sklearn
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        build-essential \
        gcc \
        g++ \
        ffmpeg \
        libopenblas-dev \
        liblapack-dev \
        libblas-dev \
        && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU FIRST (cached wheel)
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --upgrade-strategy only-if-needed \
    -r requirements.txt

COPY app ./app

ENV STORAGE_DIR=/app/storage

RUN mkdir -p /app/storage/uploads /app/storage/logs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
