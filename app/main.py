import requests
import json
import os
import random


class PokeAPI:
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

    def _get_poke_base_data(self, poke_index=1) -> dict:
        poke_res = requests.get(os.path.join(self.POKE_API_BASE_URI, str(poke_index)))
        poke_data = poke_res.json()

        return {
            "name": poke_data["name"],
            "image": poke_data["sprites"]["front_default"],
            "weight_kg": poke_data["weight"] / 10,  # HG a KG
            "types": [p["type"]["name"] for p in poke_data["types"]],
            "species_url": poke_data["species"]["url"],
        }

    def _get_species_data(self, species_url):
        specie_data = self._request_data(species_url)
        return {
            "color": specie_data["color"]["name"],
            "is_baby": specie_data["is_baby"],
            "is_legendary": specie_data["is_legendary"],
            "is_mythical": specie_data["is_mythical"],
            "varieties_name": [v["pokemon"]["name"] for v in specie_data["varieties"]],
            "evolution_chain_url": specie_data["evolution_chain"]["url"],
        }

    def get_poke_info(self, poke_index=1) -> dict:
        pokemon_base_data = self._get_poke_base_data(poke_index)
        species_url = pokemon_base_data.pop("species_url")

        species_data = self._get_species_data(species_url)
        evolution_chain_url = species_data.pop("evolution_chain_url")

        evos_data = self._request_data(evolution_chain_url)
        evolution_names = self._get_evolution_names(evos_data["chain"])

        pokemon_info = {
            **pokemon_base_data,
            **species_data,
            "evos": evolution_names,
        }

        return pokemon_info


poke = PokeAPI()

POKEDEX_NUM = 1025
POKE_NUM = 30
poke_ids = random.sample(range(1, POKEDEX_NUM + 1), POKE_NUM)
poke_list = [poke.get_poke_info(id) for id in poke_ids]

# while len(poke_ids) < 30:
#     num = random.randint(1, 1025)
#     if num not in poke_ids:
#         poke_ids.append(num)
#         poke_list.append(poke.get_poke_info(num))


file_name = os.path.join(os.getcwd(), "app/data/data.json")

with open(file_name, "w") as data_json:
    json.dump(poke_list, data_json, indent=2)


# https://www.datacamp.com/es/tutorial/python-private-methods-explained?dc_referrer=https%3A%2F%2Fwww.google.com%2F
# Codigo Anterior de obtener las veoluciones de manera statica
# evo_ruta = evos_data["chain"]["evolves_to"][0]
# if evo_ruta["species"]["name"]:
#     evos.append(evo_ruta["species"]["name"])
#     if evo_ruta["evolves_to"][0]["species"]:
#         evos.append(evo_ruta["evolves_to"][0]["species"]["name"])
# Metodo para obtener el index a partir de el nombre del elemento y eliminarlo de la lista
# evos.pop(evos.index(name))
