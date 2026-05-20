FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libreoffice-writer && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .
COPY data/ ./data/

RUN mkdir -p /app/output

ENV DATA_DIR=/app/data
ENV OUTPUT_DIR=/app/output

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]
