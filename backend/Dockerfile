FROM python:3.12

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set default PORT environment variable to 10000 (Render default)
ENV PORT=10000
EXPOSE $PORT

# Execute uvicorn with shell form so $PORT gets expanded properly
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT