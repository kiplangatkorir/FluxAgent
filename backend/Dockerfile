FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU version first to avoid downloading CUDA dependencies  
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch

COPY requirements.txt .
# Install requirements with PyTorch CPU index as extra index
# This ensures pip prefers CPU versions if it needs to resolve torch dependencies
# --upgrade-strategy only-if-needed prevents reinstalling torch if already satisfied
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --upgrade-strategy only-if-needed \
    -r requirements.txt

COPY app ./app

ENV STORAGE_DIR=/app/storage

RUN mkdir -p /app/storage/uploads /app/storage/logs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

