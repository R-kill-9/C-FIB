from numpy import *
file = open('E9r-v17Y', 'r')
characters = file.read() 
num_chars = len(characters)
print("Total characters: ")
print(num_chars)
print("Possible options:")
for i in range(100, 201):
    if num_chars%i == 0:
        print(i)
        columns = i
        #si es multiplo es una opcion
        rows = int(num_chars/i)
        option = zeros((rows,columns), dtype = str)
        for j in range(rows):
            for k in range(columns):
                option[j][k] = characters[j * columns + k]
        #print
        for a in range(columns):
            for b in range(rows):
                #print(option[a][b], end ='')
                file = open(str(i)+"solutioni.txt", 'a')
                file.write(option[b][a])
