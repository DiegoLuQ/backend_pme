import random
import uuid
# Generar un número aleatorio entre 0 y 1 y convertirlo en una cadena

def id_random():
    u = uuid.uuid1()
    return u

# print(id_random())

def num_random():
    # Generar un número aleatorio entre 0 y 1 y convertirlo en una cadena
    rand_num = str(random.random())[2:]

    # Generar una secuencia de 6 dígitos aleatorios y concatenarla con el número aleatorio
    id = rand_num + str(random.randint(100000, 999999))
    return id

# print(num_random())