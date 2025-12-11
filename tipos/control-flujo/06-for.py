buscar = 10
for numero in range(5):
    print(numero)
    if numero == buscar:
        break
    print("encontrado", buscar)
else:
    print("no encontre el numero buscado :(")
