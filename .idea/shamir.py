import random
from functools import reduce

def generar_coeficientes(k, primo):
    return [random.randint(1, primo - 1) for _ in range(k - 1)]

def evaluar_polinomio(x, coeficientes, primo):
    return sum([coef * (x ** i) for i, coef in enumerate(coeficientes)]) % primo

def generar_partes(S, n, k, primo):
    coeficientes = [S] + generar_coeficientes(k, primo)
    
    partes = [(i, evaluar_polinomio(i, coeficientes, primo)) for i in range(1, n + 1)]
    
    return partes

def inverso_modular(x, primo):
    g, a, _ = algoritmo_extendido_de_euclides(x, primo)
    if g != 1:
        raise ValueError("No existe inverso modular")
    return a % primo

def algoritmo_extendido_de_euclides(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = algoritmo_extendido_de_euclides(b % a, a)
        return g, y - (b // a) * x, x

def interpolacion_lagrange(x, x_s, y_s, primo):
    def PI(vals):
        return reduce(lambda x, y: x * y % primo, vals, 1)
    
    total = 0
    k = len(x_s)
    
    for j in range(k):
        otros = list(x_s)
        cur_x = otros.pop(j)
        
        numerador = PI([x - o for o in otros]) % primo
        denominador = PI([cur_x - o for o in otros]) % primo
        
        coef_lagrange = numerador * inverso_modular(denominador, primo) % primo
        total = (total + y_s[j] * coef_lagrange) % primo
    
    return total

def reconstruir_secreto(partes, primo):
    x_s, y_s = zip(*partes)  
    return interpolacion_lagrange(0, x_s, y_s, primo)

S = int(input("Ingrese el secreto (S): "))
n = int(input("Ingrese el número total de partes (n): "))
k = int(input("Ingrese el número mínimo de partes para reconstruir (k): "))
primo = int(input("Ingrese un número primo mayor que S para la aritmética modular: "))

partes = generar_partes(S, n, k, primo)

print("\nPartes generadas:")
for parte in partes:
    print(f"Parte {parte[0]}: {parte[1]}")

num_partes_a_usar = int(input("\n¿Cuántas partes deseas usar para reconstruir el secreto? (Debe ser al menos k): "))
partes_a_reconstruir = []

for _ in range(num_partes_a_usar):
    x = int(input("Ingrese el índice de la parte (x): "))
    y = int(input(f"Ingrese el valor de la parte {x} (y): "))
    partes_a_reconstruir.append((x, y))

secreto_reconstruido = reconstruir_secreto(partes_a_reconstruir, primo)
print("\nEl secreto reconstruido es:", secreto_reconstruido)

