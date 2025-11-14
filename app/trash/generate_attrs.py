# Genrerar atributos de validadro a los pokemons


def transformar_pokemon(pokemon):
    types_lower = [t.lower() for t in pokemon.get("types", [])]
    gen = pokemon.get("generation", 0)

    # 0. ¿Es este Pokémon un Legendario, Mítico o Ultraente?
    pokemon["is_special_status"] = (
        pokemon.get("is_legendary", False)
        or pokemon.get("is_mythical", False)
        or pokemon.get("is_ultrabeast", False)
    )

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

    # Ponemos el dato de si es un pokemon de la generacion 1 o 2
    pokemon["is_gen_1_or_2"] = gen in [1, 2]

    # 5. ¿Se introdujo en una Generación par (2, 4, 6, 8)?
    pokemon["is_gen_even"] = gen > 0 and gen % 2 == 0

    # 6. ¿Tiene más de dos etapas evolutivas en total (una línea de 3 o más Pokémon)?
    pokemon["is_three_stage_evo"] = len(pokemon.get("evos", [])) >= 3

    # 7. ¿No tiene evoluciones (es una etapa única, no Legendario/Mítico)?
    is_single_stage = len(pokemon.get("evos", [])) == 1
    pokemon["is_single_stage_non_special"] = (
        is_single_stage and not pokemon["is_special_status"]
    )

    # 8. ¿Posee alguna Forma Regional (ej. de Alola, Galar o Paldea)?
    # pokemon["has_regional_form"] = pokemon.get("has_regional_form", False)

    # 9. ¿Se encuentra de forma silvestre principalmente en una Región nevada o desértica?
    # pokemon["is_habitat_snow_or_desert"] = pokemon.get(
    #     "is_habitat_snow", False
    # ) or pokemon.get("is_habitat_desert", False)

    # 10. ¿Su Color predominante es el Rojo, Azul o Verde?
    color = pokemon.get("color", "").lower()
    pokemon["is_color_rgb"] = color in ["red", "blue", "green"]

    # 11. ¿Su Color predominante es el Amarillo, Violeta o Rosa?
    pokemon["is_color_yellow_purple_pink"] = color in ["yellow", "purple", "pink"]

    # 12. ¿Pesa más de 200 kg?
    weight = pokemon.get("weight_kg", 0)
    pokemon["weight_over_200kg"] = weight > 200

    # 13. ¿Pesa menos de 1 kg?
    pokemon["weight_under_1kg"] = weight < 1 and weight > 0

    # 14. ¿Aprende un Ataque único (movimiento característico)?
    # pokemon["has_signature_move"] = pokemon.get("has_signature_move", False)

    # 15. ¿Su Nombre en tiene más de 7 letras?
    pokemon["name_len_over_7"] = len(pokemon.get("name", "")) > 7

    # 16. ¿Su Nombre en español empieza con una consonante?
    name_upper = pokemon.get("name", "").upper()
    consonants = "BCDFGHJKLMNÑPQRSTVWXYZ"
    pokemon["name_starts_consonant"] = name_upper and name_upper[0] in consonants

    # 17. ¿Es de Tipo Bicho o Tipo Veneno y pertenece a la Generación 7 o posterior?
    is_bug_or_poison = "bug" in types_lower or "poison" in types_lower
    is_gen_7_plus = gen >= 7
    pokemon["is_bug_poison_gen_7_plus"] = is_bug_or_poison and is_gen_7_plus

    # 18. ¿Es un Pokémon que puede Megaevolucionar?
    # pokemon["can_mega_evolve"] = pokemon.get("can_mega_evolve", False)

    # 19. ¿Es un Pokémon Legendario con una Forma Regional?
    # is_legendary = pokemon.get("is_legendary", False)
    # has_regional_form = pokemon.get("has_regional_form", False)
    # pokemon["is_legendary_with_regional_form"] = is_legendary and has_regional_form

    return pokemon
