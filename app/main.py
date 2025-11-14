from flask import Flask, request, render_template, url_for
import json
import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    # Cargar JSON de pokemons
    ruta_json = os.path.join(app.root_path, "data", "data.json")

    with open(ruta_json, "r", encoding="utf-8") as f:
        pokemons = json.load(f)

    # Renderiza index.html que extiende base.html
    return render_template("index.html", pokemons=pokemons)


@app.route("/preguntas", methods=["GET", "POST"])
def preguntas():
    if request.method == "POST":
        # Recoger la respuesta del usuario si viene del formulario
        respuesta = request.form.get("respuesta")
        # Aquí podrías procesarla o guardarla si hace falta

    return render_template("preguntas.html")


@app.route("/resultado")
def resultado():
    pokemon = request.args.get("pokemon", "Desconocido")
    return render_template("resultado.html", pokemon=pokemon)


if __name__ == "__main__":
    app.run(debug=True)
