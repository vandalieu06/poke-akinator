import requests
import json
import os


class PokeAPi:
    POKE_API_BASE_URI = "https://pokeapi.co/api/v2/pokemon/"

    def __init__(self):
        print("[LOG] Utilizando PokeApi")

    def _request_data(self, url: str) -> dict:
        response = requests.get(url)
        return response.json()

    def _get_evolution_names(self, evos_data: dict) -> list:
        def extract_evolution_names(evolution_steep: dict, evolution_list: list):
            if "species" in evolution_steep:
                evolution_list.append(evolution_steep["species"]["name"])
            for next_steep in evolution_steep.get("evolves_to", []):
                extract_evolution_names(next_steep, evolution_list)

        evolution_list = []
        extract_evolution_names(evos_data, evolution_list)
        return evolution_list

    def get_poke_info(self, poke_index=1) -> dict:
        poke_res = requests.get(os.path.join(self.POKE_API_BASE_URI, str(poke_index)))
        poke_data = poke_res.json()

        name = poke_data["name"]
        image = poke_data["sprites"]["back_default"]
        weight_kg = poke_data["weight"] / 10  # HG a KG
        types = [p["type"]["name"] for p in poke_data["types"]]

        specie_data = self._request_data(poke_data["species"]["url"])

        color = specie_data["color"]["name"]
        is_baby = specie_data["is_baby"]
        is_legendary = specie_data["is_legendary"]
        is_mythical = specie_data["is_mythical"]
        varieties_name = [v["pokemon"]["name"] for v in specie_data["varieties"]]

        evos_data = self._request_data(specie_data["evolution_chain"]["url"])
        evos = self._get_evolution_names(evos_data["chain"])

        pokemon_info = {
            "name": name,
            "image": image,
            "weight_kg": weight_kg,
            "types": types,
            "color": color,
            "is_baby": is_baby,
            "is_legendary": is_legendary,
            "is_mythical": is_mythical,
            "varieties": varieties_name,
            "evos": evos,
        }
        return pokemon_info


poke = PokeAPi()
poke_info = poke.get_poke_info(777)
print(json.dumps(poke_info, indent=2))
# https://www.datacamp.com/es/tutorial/python-private-methods-explained?dc_referrer=https%3A%2F%2Fwww.google.com%2F
# Codigo Anterior de obtener las veoluciones de manera statica
# evo_ruta = evos_data["chain"]["evolves_to"][0]
# if evo_ruta["species"]["name"]:
#     evos.append(evo_ruta["species"]["name"])
#     if evo_ruta["evolves_to"][0]["species"]:
#         evos.append(evo_ruta["evolves_to"][0]["species"]["name"])
# Metodo para obtener el index a partir de el nombre del elemento y eliminarlo de la lista
# evos.pop(evos.index(name))
