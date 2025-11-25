from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.utils.data_handler import DataHandler
from app.utils.game import PokeAkinatorLogic
from app.utils.generate_poke_data import generate_new_pokemon_data

game_bp = Blueprint("game", __name__)


# Funciones Auxiliares


def init_game():
    """Genera nuevos datos de Pokémon y reinicia la sesión del juego."""
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

        current_app.logger.info(f"Lista IDS: {list(range(len(poke_data)))}")
    return poke_data


def load_game():
    """Carga el estado del juego desde la sesión y lo mapea a la clase de lógica."""
    if "game" not in session:
        return None, None

    data_loader = DataHandler()
    poke_data = data_loader.get_data("data.json")
    questions_data = data_loader.get_data("questions.json")

    if poke_data is not None and questions_data is not None:
        game = PokeAkinatorLogic(poke_data, questions_data)
        current_pokes = session["game"]["current_poke_indices"]
        game.current_poke_data = [poke_data[p] for p in current_pokes]
        game.current_question_index = session["game"]["current_question_index"]
        game.history = session["game"]["history"]
        return game, poke_data
    return None, None


def save_game(game, poke_data):
    """Guarda el estado actual del juego de vuelta a la sesión."""
    current_pokes = [poke_data.index(p) for p in game.current_poke_data]
    current_app.logger.info(current_pokes)
    session["game"] = {
        "current_poke_indices": current_pokes,
        "current_question_index": game.current_question_index,
        "history": game.history,
    }


# Rutas


@game_bp.route("/", methods=["GET"])
def index():
    poke_data = init_game()
    return render_template("index.html", pokemons=poke_data)


@game_bp.route("/restart")
def restart():
    init_game()
    return redirect(url_for("game.index"))  # Usa game.index


@game_bp.route("/preguntas", methods=["GET", "POST"])
def question():
    game, poke_data = load_game()

    if game is None:
        return redirect(url_for("game.index"))  # Usa game.index

    if game.is_game_over():
        return redirect(url_for("game.resultado"))  # Usa game.resultado

    if request.method == "POST":
        user_answer = request.form.get("respuesta")
        _, filter_key = game.get_current_question()
        game.process_answer(user_answer, filter_key)

        save_game(game, poke_data)

        if game.is_game_over():
            return redirect(url_for("game.resultado"))  # Usa game.resultado

    question_text, _ = game.get_current_question()

    return render_template(
        "preguntas.html", question=question_text, index=game.current_question_index + 1
    )


@game_bp.route("/resultado")
def resultado():
    game, poke_data = load_game()
    if game is None:
        return redirect(url_for("game.index"))

    result_text = game.get_result()

    if not result_text:
        candidates = ", ".join([p["name"] for p in game.current_poke_data])
        result_text = f"Posibles candidatos: {candidates}"

    current_app.logger.info(f"[LOG] POKE IDS ACTUALES: {game.current_poke_data}")

    if len(game.current_poke_data) != 1:
        return render_template(
            "resultado.html", result=result_text, poke_img="/static/img/who_is_poke.png"
        )

    return render_template(
        "resultado.html",
        result=result_text,
        poke_img=game.current_poke_data[0]["image"],
    )
