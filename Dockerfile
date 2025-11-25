FROM python:3.13.3-slim
WORKDIR /server
COPY requeriments.txt .
RUN pip install --no-cache-dir -r requeriments.txt
WORKDIR /server/app
COPY ./app .
EXPOSE 5000
WORKDIR /server
CMD ["python", "-m", "app.main"]
