import asyncio
import httpx
import json
import os
import random
import time
from typing import Dict, Any

POKE_API_BASE_URI = "https://pokeapi.co/api/v2/pokemon/"
POKEDEX_NUM = 1025
POKE_NUM = 30


class AsyncPokeAPI:
    """Clase refactorizada para usar peticiones asíncronas con httpx."""

    def __init__(self):
        print("[LOG] Utilizando AsyncPokeAPI - Concurrencia activada.")

    async def _request_data(self, client: httpx.AsyncClient, url: str):
        """Realiza una solicitud asíncrona usando el cliente de sesión."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"[ERROR] HTTP Error for {url}: {e.response.status_code}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2**attempt)
            except httpx.RequestError as e:
                print(f"[ERROR] Request Error for {url}: {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2**attempt)
        return {}

    def _get_evolution_names(self, evos_data: dict):
        """Extrae de forma recursiva los nombres de la cadena de evolución."""

        def extract_evolution_names(evolution_steep: dict, evolution_list: list):
            if "species" in evolution_steep:
                evolution_list.append(evolution_steep["species"]["name"])
            for next_steep in evolution_steep.get("evolves_to", []):
                extract_evolution_names(next_steep, evolution_list)

        evolution_list = []
        extract_evolution_names(evos_data, evolution_list)
        return evolution_list

    async def _get_poke_base_data(self, client: httpx.AsyncClient, poke_index: int):
        """Obtiene datos base del Pokémon (Paso 1)."""
        url = os.path.join(POKE_API_BASE_URI, str(poke_index))
        poke_data = await self._request_data(client, url)

        return {
            "name": poke_data["name"],
            "image": poke_data["sprites"]["front_default"],
            "weight_kg": poke_data["weight"] / 10,  # HG a KG
            "types": [p["type"]["name"] for p in poke_data["types"]],
            "species_url": poke_data["species"]["url"],
        }

    async def _get_species_data(self, client: httpx.AsyncClient, species_url: str):
        """Obtiene datos de la especie (Paso 2)."""
        specie_data = await self._request_data(client, species_url)

        return {
            "color": specie_data["color"]["name"],
            "is_baby": specie_data["is_baby"],
            "is_legendary": specie_data["is_legendary"],
            "is_mythical": specie_data["is_mythical"],
            "varieties_name": [v["pokemon"]["name"] for v in specie_data["varieties"]],
            "evolution_chain_url": specie_data["evolution_chain"]["url"],
            "generation_url": specie_data["generation"]["url"],
        }

    async def _get_generation_id(self, client: httpx.AsyncClient, gen_url: str):
        """Obtiene el ID de la generación (Paso 3)."""
        gen_data = await self._request_data(client, gen_url)
        return {"generation": gen_data["id"]}

    async def _get_evolution_names_from_url(
        self, client: httpx.AsyncClient, evolution_chain_url: str
    ):
        """Obtiene los datos de la cadena de evolución y extrae los nombres (Paso 4)."""
        evos_data = await self._request_data(client, evolution_chain_url)
        return self._get_evolution_names(evos_data["chain"])

    def _add_derived_attributes(self, pokemon: Dict[str, Any]):
        """Genera atributos de validación y de estado derivados de los datos obtenidos (Paso 5)."""

        types_lower = [t.lower() for t in pokemon.get("types", [])]
        gen = pokemon.get("generation", 0)
        color = pokemon.get("color", "").lower()
        weight = pokemon.get("weight_kg", 0)

        # 0. ¿Es este Pokémon un Legendario o Mítico? (No podemos obtener Ultra Beasts o Formas Regionales con solo estas llamadas)
        pokemon["is_special_status"] = pokemon.get(
            "is_legendary", False
        ) or pokemon.get("is_mythical", False)

        # 1. ¿Su Tipo principal es Normal, Planta o Agua?
        main_type = types_lower[0] if types_lower else None
        pokemon["is_main_type_normal_grass_water"] = main_type in [
            "normal",
            "grass",
            "water",
        ]

        # 2. ¿Tiene un doble Tipo Elemento (es decir, más de uno)?
        pokemon["has_dual_type"] = len(types_lower) > 1

        # 3. ¿Su Tipo secundario es Volador, Hada o Acero?
        secondary_type = types_lower[1] if len(types_lower) > 1 else None
        pokemon["is_secondary_type_flying_fairy_steel"] = secondary_type in [
            "flying",
            "fairy",
            "steel",
        ]

        # 4. ¿Es un Pokémon de la Generación 1 o 2?
        pokemon["is_gen_1_or_2"] = gen in [1, 2]

        # 5. ¿Se introdujo en una Generación par (2, 4, 6, 8)?
        pokemon["is_gen_even"] = gen > 0 and gen % 2 == 0

        # 6. ¿Tiene más de dos etapas evolutivas en total?
        pokemon["is_three_stage_evo"] = len(pokemon.get("evos", [])) >= 3

        # 7. ¿No tiene evoluciones (es una etapa única, no Legendario/Mítico)?
        is_single_stage = len(pokemon.get("evos", [])) == 1
        pokemon["is_single_stage_non_special"] = (
            is_single_stage and not pokemon["is_special_status"]
        )

        # 10. ¿Su Color predominante es el Rojo, Azul o Verde?
        pokemon["is_color_rgb"] = color in ["red", "blue", "green"]

        # 11. ¿Su Color predominante es el Amarillo, Violeta o Rosa?
        pokemon["is_color_yellow_purple_pink"] = color in ["yellow", "purple", "pink"]

        # 12. ¿Pesa más de 200 kg?
        pokemon["weight_over_200kg"] = weight > 200

        # 13. ¿Pesa menos de 1 kg?
        pokemon["weight_under_1kg"] = weight < 1 and weight > 0

        # 15. ¿Su Nombre tiene más de 7 letras?
        pokemon["name_len_over_7"] = len(pokemon.get("name", "")) > 7

        # 16. ¿Su Nombre en inglés empieza con una consonante? (Nota: Los nombres de PokeAPI están en inglés)
        name_upper = pokemon.get("name", "").upper()
        # Consonantes del alfabeto inglés: B, C, D, F, G, H, J, K, L, M, N, P, Q, R, S, T, V, W, X, Y, Z.
        consonants = "BCDFGHJKLMNPQRSTVWXYZ"
        pokemon["name_starts_consonant"] = name_upper and name_upper[0] in consonants

        # 17. ¿Es de Tipo Bicho o Tipo Veneno y pertenece a la Generación 7 o posterior?
        is_bug_or_poison = "bug" in types_lower or "poison" in types_lower
        is_gen_7_plus = gen >= 7
        pokemon["is_bug_poison_gen_7_plus"] = is_bug_or_poison and is_gen_7_plus

        # Atributos no implementables sin más peticiones:
        # 8. has_regional_form (Requiere revisar la lista de variedades y compararla con el nombre base, lo cual es más complejo)
        # 9. is_habitat_snow_or_desert (El endpoint de 'species' ya no provee datos de 'habitat')
        # 14. has_signature_move (Requiere peticiones adicionales a 'moves')
        # 18. can_mega_evolve (Requiere peticiones a 'forms' o 'moves')
        # 19. is_legendary_with_regional_form (Depende del punto 8)

        return pokemon

    async def get_poke_info(self, client: httpx.AsyncClient, poke_index: int):
        """Función principal que orquesta todas las peticiones y añade los atributos derivados."""

        pokemon_base_data = await self._get_poke_base_data(client, poke_index)

        species_url = pokemon_base_data.pop("species_url")
        species_data = await self._get_species_data(client, species_url)

        evolution_chain_url = species_data.pop("evolution_chain_url")
        generation_url = species_data.pop("generation_url")

        gen_task = self._get_generation_id(client, generation_url)
        evos_task = self._get_evolution_names_from_url(client, evolution_chain_url)

        gen_id, evolution_names = await asyncio.gather(gen_task, evos_task)

        pokemon_info = {
            **pokemon_base_data,
            **species_data,
            **gen_id,
            "evos": evolution_names,
        }

        final_pokemon_info = self._add_derived_attributes(pokemon_info)

        return final_pokemon_info


async def main():
    start_time = time.time()

    poke = AsyncPokeAPI()

    poke_ids = random.sample(range(1, POKEDEX_NUM + 1), POKE_NUM)
    print(f"[INFO] Buscando y transformando información para {POKE_NUM} Pokémons...")

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [poke.get_poke_info(client, id) for id in poke_ids]
        poke_list = await asyncio.gather(*tasks)

    file_dir = os.path.join(os.getcwd(), "data")
    file_name = os.path.join(file_dir, "data.json")

    with open(file_name, "w") as data_json:
        json.dump(poke_list, data_json, indent=2)

    end_time = time.time()

    print(f"\n[ÉXITO] Datos de {len(poke_list)} Pokémons guardados en '{file_name}'")
    print(f"[TIEMPO TOTAL] {end_time - start_time:.2f} segundos.")


if __name__ == "__main__":
    asyncio.run(main())
