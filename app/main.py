from app import create_app

# Para Desarollo
app = create_app()
if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"])

# Para Despliegue
# app = create_app('config.ProductionConfig')
