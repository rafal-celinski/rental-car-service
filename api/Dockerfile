FROM python:3.10

WORKDIR /api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
