from app.utils.data_handler import DataHandler
from app.utils.game import PokeAkinatorLogic

RESPUESTAS_POSITIVAS = {"Y", "y", "S", "s"}
RESPUESTAS_NEGATIVAS = {"N", "n"}


def run_console_game():
    # Cargamos los datos
    print("[LOG] Iniciando carga de datos...")
    data_loader = DataHandler()
    poke_data = data_loader.get_data("data.json")
    questions_data = data_loader.get_data("questions.json")

    # Verificamos que hay datos
    if not poke_data or not questions_data:
        print("[ERROR] No se pudieron cargar los datos. Terminando.")
        return

    # Iniciamos el juego con lo datos
    game = PokeAkinatorLogic(poke_data, questions_data)
    print("\n[LOG] ¡Juego de PokeAkinator iniciado!")

    # Recoremos los pokemons y obtenemos los nombres
    pokes = [p["name"] for p in game.all_poke_data]
    print("Escoge uno de los siguientes pokemons: " + ", ".join(pokes))

    # Bucle de preguntas mientras no haya mas pokemons/preguntas
    while not game.is_game_over():
        # Obtenemos la pregunta actual y la informacion correspondiente
        current_question_info = game.get_current_question()

        if current_question_info is None:
            print("[LOG] No hay más preguntas disponibles.")
            break

        question, filter_key = current_question_info

        # Esperamos respuesta usuario y verificamos que sea valida
        res_user = input(
            f"\n{game.current_question_index + 1} - {question} (Y/S o N): "
        )

        if res_user.strip() not in (RESPUESTAS_POSITIVAS | RESPUESTAS_NEGATIVAS):
            print("[ERROR] Respuesta no válida, por favor usa Y/S o N.")
            continue

        game.process_answer(res_user, filter_key)

        if len(game.current_poke_data) == 1:
            print(f"\n[FIN] ¡Tu Pokémon es {game.current_poke_data[0]['name']}!")
            break

    final_message = game.get_result()
    if final_message:
        print(f"\n--- RESULTADO ---\n{final_message}")
    else:
        candidates = ", ".join([p["name"] for p in game.current_poke_data])
        print(
            f"\n[FIN] ¡Se acabaron las preguntas! Los posibles candidatos son: {candidates}"
        )
