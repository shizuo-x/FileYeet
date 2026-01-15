FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create directories for mounting
RUN mkdir -p /data/input /data/output

EXPOSE 8336

CMD ["python", "app.py"]