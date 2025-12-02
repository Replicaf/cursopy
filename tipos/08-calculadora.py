n1 = input("Ingrese el primer número: ")
n2 = input("Ingrese el segundo número: ")

n1 = int(n1)
n2 = int(n2)
suma = n1 + n2
resta = n1 - n2
multiplicacion = n1 * n2
division = n1 / n2

mensaje = f"""
para los números {n1} y {n2},
el resultado de la suma es: {suma},
el resultado de la resta es: {resta} ,
el resultado de la multiplicación es {multiplicacion},
el resultado de la división es: {division}  
"""

print(mensaje)
