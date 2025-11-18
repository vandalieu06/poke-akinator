from flask import Flask, render_template, request, session, redirect, url_for
from utils.game import DataHandler, PokeAkinatorLogic

app = Flask(__name__)
app.secret_key = "86d27b0aaa812eee1b0d607355b1eaf96c4ebd955cc4f72523543535a109b671"


def init_game():
    data_loader = DataHandler()
    poke_data = data_loader.get_data("data.json")
    questions_data = data_loader.get_data("questions.json")

    session["game"] = {
        "current_poke_indices": list(range(len(poke_data))),
        "current_question_index": 0,
        "history": []
    }


def load_game():
    if "game" not in session:
        return None, None

    data_loader = DataHandler()
    poke_data = data_loader.get_data("data.json")
    questions_data = data_loader.get_data("questions.json")

    game = PokeAkinatorLogic(poke_data, questions_data)

    indices = session["game"]["current_poke_indices"]
    game.current_poke_data = [poke_data[i] for i in indices]
    game.current_question_index = session["game"]["current_question_index"]
    game.history = session["game"]["history"]

    return game, poke_data


def save_game(game, poke_data):
    indices = [poke_data.index(p) for p in game.current_poke_data]
    session["game"] = {
        "current_poke_indices": indices,
        "current_question_index": game.current_question_index,
        "history": game.history
    }


@app.route("/", methods=["GET"])
def index():
    if "game" not in session:
        init_game()

    data_loader = DataHandler()
    poke_data = data_loader.get_data("data.json")

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
        "preguntas.html",
        question=question_text,
        index=game.current_question_index + 1
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

    return render_template("resultado.html", result=result_text, pokemon=game.current_poke_data[0]["image"])


if __name__ == "__main__":
    app.run(debug=True)