#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys

from timeit import default_timer as timer

caching = {}

def similarity(a, b):
    '''
    Efectua un calculo de similitud basado en SMC (Simple Matching Coefficient)
    SMC nos permite obtener la similitud entre vectores binarios
    '''
    match = 0
    sample_a = a.split(',')
    sample_b = b.split(',')
    size = len(sample_a)-1

    if a + b in caching:
        return caching[a + b]

    # Comparamos todos los atributos
    for index in range(0, size-1):
        if sample_a[index].strip() == sample_b[index].strip():
            match += 1

    # Redondeamos a dos decimales
    score = round(float(match)/float(size), 2)
    caching[a + b] = score
    return score


def get_score(matrix, medoids):
    '''
    Funcion de scoring general, dependiente de la asignacion de la funcion
    similarity. Devuelve los valores categorizados y la puntuacion obtenida.
    '''
    # Iniciamos variables
    score = 0.0
    clusters = {}

    # Creamos un nuevo espacio de clusters. Las claves son indices.
    for medoid in medoids:
        clusters[medoid] = []

    # Iteramos sobre la matrix de datos
    for non_medoid in range(len(matrix)):
    # Evitamos comparar medoides con medoides
        if non_medoid in medoids:
            continue

        # Iniciamos variables para escoger el cluster adecuado
        result = -1.0
        selected_medoid = None

        # Iteramos sobre los medoides (indices) y adjudicamos el mejor cluster
        for medoid in medoids:
            tmp_result = similarity(matrix[medoid], matrix[non_medoid])
            if tmp_result > result:
                result = tmp_result
                selected_medoid = medoid

        clusters[selected_medoid].append(non_medoid)
        score += result

    return (clusters, score)


def get_class(matrix, item):
    '''
    Funcion de utilidad que extrae la clase de cada elemento
    '''
    return matrix[item].split(',')[-1].strip()


def pam(matrix, k):
    '''
    Funcion principal que implementa el algoritmo PAM.
    Acepta una matrix de datos, el numero de clusters y el numero maximo de
    iteraciones.
    '''

    # Iniciamos el crono para medir el tiempo de ejecucion
    start = timer()

    # Inicializamos y escogemos k medoides iniciales de forma aleatoria
    medoids = []
    for i in range(k):
        medoids.append(random.randint(0, len(matrix)-1))

    # Obtenemos el score y los clusteres iniciales
    clusters, score = get_score(matrix, medoids)


    # Iteramos hasta que la puntuacion (score) no mejore
    iterations = 0
    while True:
        # Recorremos los clusters
        for medoid in clusters:
            # Creamos una copia de la lista de medoides actual
            medoids_copy = medoids[:]
            # Quitamos el medoide actual de la copia de la lista de medoides
            medoids_copy.remove(medoid)
            # Recorremos los no medoides del cluster
            for no_medoid in clusters[medoid]:
                # Agregamos el nuevo candidato a medoide
                medoids_copy.append(no_medoid)
                # Obtenemos los nuevos clusters y puntuacion
                new_clusters, new_score = get_score(matrix, medoids_copy)
                # Si mejoramos la puntuacion nos quedamos con los nuevos
                if score < new_score:
                    clusters = new_clusters
                    score = new_score
                    medoids = medoids_copy[:]
                    print "Iteration: \t%s\tScore: %s" % (iterations, score)
                # Borramos el medoide candidato de la copia de la lista
                medoids_copy.remove(no_medoid)
                # Terminamos con la iteracion actual
                iterations += 1
        # Hemos terminado de recorrer los clusters, miramos si la puntuacion mejora
        # En caso contrario salimos
        if score > new_score:
            break

    # Detenemos crono para medicion de tiempo de ejecucion
    end = timer()
    print ""
    print "Running time: %s seconds" % round(end - start, 2)

    # Imprimimos informacion de resultados
    resume(clusters, len(matrix))


def resume(clusters, length):
    '''
    Funcion resumen que muestra el porcentaje de acierto por cluster y otros
    valores de rendimiento y la matriz de confusion.
    '''
    print ""
    print "Confusion Matrix"
    print "----------------"
    print ""
    print "Class\t|\t<=50K\t|\t>50K"
    print "-------------------------------------"

    total_poor = 0
    total_rich = 0
    for i, item in enumerate(clusters):
        rich = 0
        poor = 0
        for entry in clusters[item]:
            if get_class(matrix, entry) == '<=50K':
                poor += 1
            elif get_class(matrix, entry) == '>50K':
                rich += 1
        if poor > rich:
            print "<=50K\t|\t%s\t|\t%s" % (poor, rich)
            total_poor += poor
        else:
            print ">50K\t|\t%s\t|\t%s" % (poor, rich)
            total_rich += rich

    print ""
    print "Total accuracy:\t%s" % round(float(total_poor+total_rich)/length, 2)


'''
Llamada principal.
Por defecto el numero de clusters es 2. Es posible indicar un numero como
primer parametro.
'''
if __name__  == '__main__':
    with open('candidates.data.csv', 'r') as f:
        matrix = f.readlines()
    try:
        k = int(sys.argv[1])
    except:
        k = 2

    # Invocamos a la funcion principal, con los datos (matrix), el numero de
    # clustes (k) y el nivel maximo de iteraciones.
    pam(matrix, k)
