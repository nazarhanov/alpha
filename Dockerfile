FROM python:3.9-alpine

EXPOSE 8000
WORKDIR /app

COPY src/requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt
COPY src .

CMD python3 manage.py runserver 0.0.0.0:8000
