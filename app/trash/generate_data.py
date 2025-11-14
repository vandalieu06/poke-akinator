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
        url = os.path.join(self.POKE_API_BASE_URI, str(poke_index))
        poke_data = self._request_data(url)

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
            "generation_url": specie_data["generation"]["url"],
        }

    def _get_generation_id(self, gen_url):
        gen_data = self._request_data(gen_url)
        return {"generation": gen_data["id"]}

    def get_poke_info(self, poke_index=1) -> dict:
        pokemon_base_data = self._get_poke_base_data(poke_index)
        species_url = pokemon_base_data.pop("species_url")

        species_data = self._get_species_data(species_url)
        evolution_chain_url = species_data.pop("evolution_chain_url")

        generation_url = species_data.pop("generation_url")
        gen_id = self._get_generation_id(generation_url)

        evos_data = self._request_data(evolution_chain_url)
        evolution_names = self._get_evolution_names(evos_data["chain"])

        pokemon_info = {
            **pokemon_base_data,
            **species_data,
            **gen_id,
            "evos": evolution_names,
        }

        return pokemon_info


def main():
    poke = PokeAPI()

    POKEDEX_NUM = 1025
    POKE_NUM = 30
    poke_ids = random.sample(range(1, POKEDEX_NUM + 1), POKE_NUM)
    poke_list = [poke.get_poke_info(id) for id in poke_ids]

    file_name = os.path.join(os.getcwd(), "../app/data/data.json")

    with open(file_name, "w") as data_json:
        json.dump(poke_list, data_json, indent=2)


main()
