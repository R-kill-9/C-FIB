from numpy import *
import numpy as np

# Función para convertir una tripleta de letras en una lista de números
def triplet_a_numeros(triplet):
    # Inicializar una lista vacía para almacenar los números
    numeros = []
    
    # Iterar sobre cada letra en la tripleta
    for letra in triplet:
        # Convertir la letra en un número y agregarlo a la lista
        numero = ord(letra) - 65
        numeros.append(numero)
    
    return numeros


# Función para convertir una tripleta de números en una lista de letras
def numeros_a_tripleta(numeros):
    # Inicializar una lista vacía para almacenar las letras de la tripleta
    triplet = []
    
    # Iterar sobre cada número en la lista
    for numero in numeros:
        # Convertir el número en un entero y luego en una letra, y agregarlo a la lista
        letra = chr(int(numero) + 65)
        triplet.append(letra)
    
    # Usar join para convertir la lista de letras en una cadena
    triplet_str = ''.join(triplet)
    
    return triplet_str



def main():

    file = open('text', 'r')
    characters = file.read() 
    num_chars = len(characters)
    print("Total characters: ")
    print(num_chars)
    total_perm = num_chars//3
    #diccionario para guardar cada tripleta y la cantidad de veces que sale
    permutations = {}

    # Iterar sobre el texto en grupos de tres caracteres
    for i in range(total_perm):
        triplet = characters[i * 3: (i + 1) * 3]  # Obtener la tripleta actual
        if triplet in permutations:
            permutations[triplet] += 1  # Si la tripleta ya está en el diccionario, aumenta su contador
        else:
            permutations[triplet] = 1  # Si la tripleta no está en el diccionario, agrégala con un contador de 1


    # Usar sorted para ordenar el diccionario por frecuencia de forma descendente
    sorted_permutations = sorted(permutations.items(), key=lambda x: x[1], reverse=True)

    # Tomar las tres tripletas más repetidas
    top_triplets = sorted_permutations[:3]

    # Inicializar una matriz 3x3 con ceros
    triplet_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Iterar sobre cada tripleta y asignar los valores a la matriz
    for i, triplet in enumerate([top_triplets[0][0], top_triplets[1][0], top_triplets[2][0]]):
        numeros_tripleta = triplet_a_numeros(triplet)
        for j, numero in enumerate(numeros_tripleta):
            triplet_matrix[i][j] = numero

    # Imprimir la matriz resultante
    print("Matriz mayor cantidad de tripletas:")
    for fila in triplet_matrix:
        print(fila)
    
    # Define las tripletas "AND", "ING" y "THE"
    tripleta_and = "ATT"
    tripleta_ing = "NHH"
    tripleta_the = "DAE"

    # Crea una matriz 3x3 y asigna los valores numéricos a las tripletas
    common_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    common_matrix[0] = triplet_a_numeros(tripleta_and)
    common_matrix[1] = triplet_a_numeros(tripleta_ing)
    common_matrix[2] = triplet_a_numeros(tripleta_the)

    # Imprime la common_matrix resultante
    print("Matriz tripletas comunes")
    for fila in common_matrix:
        print(fila)

    ################################# YA TENEMOS LAS DOS MATRICES ####################################
    # Verifica si la matriz es invertible (su determinante no debe ser cero)
    if np.linalg.det(common_matrix) != 0:
        # Calcula la matriz inversa
        inverse_matrix = np.linalg.inv(common_matrix)

        # Imprime la matriz inversa
        print("Matriz inversa:")
        print(inverse_matrix)
    else:
        print("La matriz no es invertible (su determinante es cero).")

    # Multiplicar la matriz inversa por triplet_matrix
    result_matrix = np.dot(inverse_matrix, triplet_matrix)

    # Imprimir la matriz resultante
    print("Resultado de la multiplicación:")
    print(result_matrix)
    


    for i in range(total_perm):
        triplet = characters[i * 3: (i + 1) * 3]  # Obtener la tripleta actual
        triplet_num = triplet_a_numeros(triplet)
        final_matrix = np.dot(result_matrix, triplet_num)
        uncrypted = numeros_a_tripleta(final_matrix)
        print(uncrypted)




if __name__ == "__main__":
    main()