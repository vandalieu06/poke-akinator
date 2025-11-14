# generate_data.py

"""
# https://www.datacamp.com/es/tutorial/python-private-methods-explained?dc_referrer=https%3A%2F%2Fwww.google.com%2F
# Codigo Anterior de obtener las veoluciones de manera statica

evo_ruta = evos_data["chain"]["evolves_to"][0]
if evo_ruta["species"]["name"]:
    evos.append(evo_ruta["species"]["name"])
    if evo_ruta["evolves_to"][0]["species"]:
        evos.append(evo_ruta["evolves_to"][0]["species"]["name"])
Metodo para obtener el index a partir de el nombre del elemento y eliminarlo de la lista
evos.pop(evos.index(name))
Metodo para verificar numeros unicos
while len(poke_ids) < 30:
    num = random.randint(1, 1025)
    if num not in poke_ids:
        poke_ids.append(num)
        poke_list.append(poke.get_poke_info(num))

"""
