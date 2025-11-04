from flask import Flask, request, render_template
import json
import os

app = Flask(__name__)


@app.route("/", methods = ["GET"])
def index():
    ruta_json = os.path.join(app.root_path, "data", "data.json")
    
    with open(ruta_json, "r", encoding="utf-8") as f:
        pokemons = json.load(f)

    return render_template("index.html", pokemons=pokemons)

@app.route('/preguntas', methods=['GET', 'POST'])
def preguntas():
    if request.method == 'POST':
        respuesta = request.form.get('respuesta')

    return render_template('preguntas.html')

@app.route('/resultado')
def resultado():
    pokemon = request.args.get('pokemon', 'Desconocido')
    return render_template('resultado.html', pokemon=pokemon)


if __name__ == "__main__":
    app.run(debug=True)
