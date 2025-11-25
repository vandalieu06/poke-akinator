from app import create_app

# Para Desarollo
app = create_app()
if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"])

# Para Despliegue
# Cuando se despliega (por ejemplo, con Gunicorn o un WSGI server),
# se llama a 'app' directamente. Por ejemplo: gunicorn run:app
# La configuración de ProductionConfig se cargaría cambiando el parámetro:
# app = create_app('config.ProductionConfig')
