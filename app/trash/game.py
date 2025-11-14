import os
import json


class PokeAkinator:
    def __init__(self):
        hello = "l"

    def _get_dir_file(self, filename):
        dir = os.path.join(os.getcwd(), "data")
        file = os.path.join(dir, filename)
        return file

    def _get_data(self, filename):
        dir = self._get_dir_file(filename)
        try:
            with open(dir, "r") as f:
                file_data = json.load(f)
                return file_data
        except FileNotFoundError as e:
            print(f"[ERROR] Archivo no encontrado: {e}")
            return False

    def _action_res_question_user(self, res_user, filter_key, poke_data):
        if res_user in ["Y", "y", "S", "s"]:
            current_poke_data = [p for p in poke_data if p.get(filter_key, False)]

        elif res_user in ["N", "n"]:
            current_poke_data = [p for p in poke_data if not p.get(filter_key, False)]

        return current_poke_data

    def start_game(self):
        # Incio del juego
        print("[LOG] START AKINATOR GAME\n")

        # Cargamos los datos del juego
        current_poke_data = self._get_data("data.json")
        questions_data = self._get_data("questions.json")

        # Introducion al juego
        print("Escoge uno de los siguientes pokemons: ")
        pokes = [p["name"] for p in current_poke_data]
        print(", ".join(pokes))

        # Logica del juego
        for i, q in enumerate(questions_data):
            if len(current_poke_data) < 1:
                print("[FIN] No hay mas pokemons, escoge uno de la lista")
                break

            if len(current_poke_data) == 2:
                print(f"Tu pokemon és {current_poke_data[0]['name']}? ")
                res_user = str(input("Respuesta: "))
                if res_user in ["Y", "y", "S", "s"]:
                    print("Fin de la partida")

                elif res_user in ["N", "n"]:
                    print(f"Tu pokemon és {current_poke_data[1]['name']}")
                    print("Fin de la partida")

                break

            current_question = questions_data[q]
            question, filter_key = current_question["question"], current_question["key"]

            res_user = str(input(f"{i + 1} - {question} (Y/y or N/n): "))

            if res_user not in ["Y", "y", "S", "s", "N", "n"]:
                print("[ERROR] Respuesta no valida, no se tendrá en cuenta.")
                continue

            current_poke_data = self._action_res_question_user(
                res_user, filter_key, current_poke_data
            )


game = PokeAkinator()
game.start_game()
