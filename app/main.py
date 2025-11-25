from flask import Flask, redirect, render_template, request, session, url_for

from app.utils.game import DataHandler, PokeAkinatorLogic
from app.utils.generate_poke_data import generate_new_pokemon_data

app = Flask(__name__)
app.secret_key = "86d27b0aaa812eee1b0d607355b1eaf96c4ebd955cc4f72523543535a109b671"


def init_game():
    try:
        generate_new_pokemon_data()
        print("[INFO] Nueva datos de Pokémons generados en app/data/data.json")
    except Exception as e:
        print(f"[ERROR] No se pudo generar nuevos datos de Pokémons: {e}")

    data_loader = DataHandler()
    poke_data = data_loader.get_data("data.json")
    if poke_data:
        session["game"] = {
            "current_poke_indices": list(range(len(poke_data))),
            "current_question_index": 0,
            "history": [],
        }

        app.logger.info(f"Lista IDS: {list(range(len(poke_data)))}")
    return poke_data


def load_game():
    if "game" not in session:
        return None, None

    data_loader = DataHandler()
    poke_data = data_loader.get_data("data.json")
    questions_data = data_loader.get_data("questions.json")

    if poke_data is not None:
        game = PokeAkinatorLogic(poke_data, questions_data)
        current_pokes = session["game"]["current_poke_indices"]
        game.current_poke_data = [poke_data[p] for p in current_pokes]
        game.current_question_index = session["game"]["current_question_index"]
        game.history = session["game"]["history"]
        return game, poke_data


def save_game(game, poke_data):
    current_pokes = [poke_data.index(p) for p in game.current_poke_data]
    app.logger.info(current_pokes)
    session["game"] = {
        "current_poke_indices": current_pokes,
        "current_question_index": game.current_question_index,
        "history": game.history,
    }


@app.route("/", methods=["GET"])
def index():
    # if "game" in session:
    #     return redirect(url_for("question"))

    poke_data = init_game()
    return render_template("index.html", pokemons=poke_data)


@app.route("/restart")
def restart():
    init_game()
    return redirect(url_for("index"))


@app.route("/preguntas", methods=["GET", "POST"])
def question():
    game, poke_data = load_game()

    if game is None:
        return redirect(url_for("index"))

    if game.is_game_over():
        return redirect(url_for("resultado"))

    if request.method == "POST":
        user_answer = request.form.get("respuesta")
        _, filter_key = game.get_current_question()
        game.process_answer(user_answer, filter_key)

        save_game(game, poke_data)

        if game.is_game_over():
            return redirect(url_for("resultado"))

    question_text, _ = game.get_current_question()

    return render_template(
        "preguntas.html", question=question_text, index=game.current_question_index + 1
    )


@app.route("/resultado")
def resultado():
    game, poke_data = load_game()
    if game is None:
        return redirect(url_for("index"))

    result_text = game.get_result()
    if not result_text:
        candidates = ", ".join([p["name"] for p in game.current_poke_data])
        result_text = f"Posibles candidatos: {candidates}"

    app.logger.info(f"[LOG] POKE IDS ACTUALES: {game.current_poke_data}")

    if len(game.current_poke_data) == 1:
        return render_template(
            "resultado.html",
            result=result_text,
            poke_img=game.current_poke_data[0]["image"],
        )
    else:
        return render_template(
            "resultado.html", result=result_text, poke_img="/static/img/who_is_poke.png"
        )


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
