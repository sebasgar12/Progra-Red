"""
Unidad II - Ejercicio 1: Hilos con nombres propios
- Crea tres hilos a partir de una lista de tuplas (nombre, cantidad_saludos).
- Guarda los objetos Thread en una lista y espera a todos con join()
  para garantizar que el mensaje final siempre aparezca al último.
"""

import threading
import time


def saludar(nombre, cantidad):
    """Imprime 'cantidad' saludos identificados con el nombre del hilo."""
    for i in range(1, cantidad + 1):
        print(f"[{nombre}] Saludo {i} de {cantidad}")
        time.sleep(0.2)


def main():
    participantes = [("Ana", 3), ("Beto", 5), ("Cora", 2)]
    hilos = []

    # Primer ciclo: crear e iniciar cada hilo guardándolo en la lista
    for nombre, cantidad in participantes:
        hilo = threading.Thread(
            target=saludar,
            args=(nombre, cantidad),
            name=nombre,
        )
        hilos.append(hilo)
        hilo.start()

    # Segundo ciclo: esperar a que cada hilo termine antes de continuar
    for hilo in hilos:
        hilo.join()

    print("Todos los hilos han terminado. Mensaje final.")


if __name__ == "__main__":
    main()
