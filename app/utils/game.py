from app.utils.data_handler import DataHandler

RESPUESTAS_POSITIVAS = {"Y", "y", "S", "s"}
RESPUESTAS_NEGATIVAS = {"N", "n"}


class PokeAkinatorLogic:
    def __init__(self, poke_data, questions_data):
        self.all_poke_data = poke_data
        self.questions_data = questions_data
        self.current_poke_data = list(poke_data)
        self.current_question_index = 0
        self.history = []

    # Paso 1 - Obtenemos la pregunta y su valor
    def get_current_question(self) -> tuple[str, str] | None:
        q_keys = list(self.questions_data.keys())

        if self.current_question_index >= len(q_keys):
            return None

        key_id = q_keys[self.current_question_index]
        question_info = self.questions_data[key_id]

        return question_info["question"], question_info["key"]

    # Paso 2 - Obtenemos la repsuesta del usuario y filtramos la lista
    def process_answer(self, res_user: str, filter_key: str) -> None:
        res = res_user.strip()

        if res in RESPUESTAS_POSITIVAS:
            self.current_poke_data = [
                p for p in self.current_poke_data if p.get(filter_key, False)
            ]
        elif res in RESPUESTAS_NEGATIVAS:
            self.current_poke_data = [
                p for p in self.current_poke_data if not p.get(filter_key, False)
            ]

        # Registra la respuesta y avanza a la siguiente pregunta
        self.history.append((filter_key, res))
        self.current_question_index += 1

    # Paso 3 - Verificamos el estado del codigo, este comprueba si no hay mas pokemon/preguntas
    def is_game_over(self) -> bool:
        return len(self.current_poke_data) <= 1 or self.get_current_question() is None

    # Paso 4 - Generamos el resultado del PokeAKinator
    def get_result(self) -> str | None:
        if not self.is_game_over():
            return None

        if len(self.current_poke_data) == 1:
            return f"¡Tu Pokémon es **{self.current_poke_data[0]['name']}**!"
        elif len(self.current_poke_data) == 0:
            return "¡No pude encontrar tu Pokémon! Parece que no está en la lista."

        return None


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
