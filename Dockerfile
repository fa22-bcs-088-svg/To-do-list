FROM python:3.9-slim
WORKDIR /app

# copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app code
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
