#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import re

# Inicializacion de constantes
candidates = []
rand = random.Random()
MAX_ENTRIES = 0
partial_less_50k = 0
partial_more_50k = 0

# Leemos el archivo y extraemos todas las entradas
with open("adult.data.csv") as f:
    print "Opening file adult.data.csv"
    data = f.readlines()

# Inicializamos MAX_ENTRIES
MAX_ENTRIES = len(data)
print "Total entries: %s" % MAX_ENTRIES


# Creamos un bucle para obtener 200 candidatos de forma aleatoria
print "Randomly selecting 200 entries..."
while not (partial_less_50k + partial_more_50k) == 200:
    index = rand.randint(0, MAX_ENTRIES - 1)
    candidate = data[index]

    # Limpiamos los campos numericos, solo extraemos campos nominales
    candidate = ",".join([field for field in candidate.split(',') if not re.match("\d.*", field)])

    # Desechamos candidatos con valores ausentes
    if '?' in candidate or len(candidate.split(',')) < 9:
        continue

    # Si el candidato no estaba ya seleccionado se escoge
    if not candidate in candidates:
        # Se comprueba a que categoria pertenece. Si ya tenemos suficientes de
        # esa categoria, simplemente se vuelve a iterar
        if candidate.split(',')[-1].strip() == "<=50K" and partial_less_50k < 100:
            candidates.append(candidate)
            partial_less_50k += 1
        elif  candidate.split(',')[-1].strip() == ">50K" and partial_more_50k < 100:
            candidates.append(candidate)
            partial_more_50k += 1

# Finalizamos y mostramos resumen al usuario
print "Finished."
print "Total selected entries %s " % len(candidates)
print "Total entries with less or 50K: %s" % partial_less_50k
print "Total entries with more than 50K: %s" % partial_more_50k
print "Dumping to file candidates.data.csv"

# Volcamos el subconjunto seleccionado a archivo
with open("candidates.data.csv", 'w') as f:
    f.writelines(candidates)


