FROM python:3.10-slim
WORKDIR /server
COPY requeriments.txt .
RUN  pip install --upgrade pip && pip install --no-cache-dir -r requeriments.txt
WORKDIR /server/app
COPY ./app .
EXPOSE 5000
WORKDIR /server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
