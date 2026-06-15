FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
      ffmpeg \
      tesseract-ocr \
      libgl1 \
      && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app

ENV TZ=Europe/Paris
ENV ARLYX_CORE_URL=http://arlyx-core:8000

EXPOSE 9000

CMD ["python", "main.py"]
