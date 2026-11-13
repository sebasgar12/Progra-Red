"""
Unidad II - Ejercicio 4: Consulta UDP con reintentos y espera creciente
- Aplica la función consultar() del Código 5 al protocolo de LA FILA.
- Envía 'CUANTOS' al servidor UDP (puerto 5001) y reintenta hasta 3 veces
  duplicando la espera en cada intento fallido: 1s, 2s y 4s -> 2**(intento - 1).
- Traduce el None final en un mensaje claro sin lanzar excepciones.
"""

import socket
import time

SERVIDOR_UDP = ("127.0.0.1", 5001)


def consultar(servidor, mensaje, reintentos=3):
    """Envía una consulta UDP y reintenta con espera exponencial (1s, 2s, 4s)."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        cliente.settimeout(2)

        for intento in range(1, reintentos + 1):
            try:
                cliente.sendto(mensaje.encode("utf-8"), servidor)
                datos, _ = cliente.recvfrom(1024)
                return datos.decode("utf-8").strip()
            except TimeoutError:
                espera = 2 ** (intento - 1)
                print(f"Intento {intento}/{reintentos}: sin respuesta. Esperando {espera}s...")
                time.sleep(espera)
            except OSError as error:
                espera = 2 ** (intento - 1)
                print(f"Intento {intento}/{reintentos}: error de red ({error}). Esperando {espera}s...")
                time.sleep(espera)

    return None


def main():
    respuesta = consultar(SERVIDOR_UDP, "CUANTOS", reintentos=3)
    if respuesta is not None:
        print(f"Respuesta del servidor LA FILA: {respuesta}")
    else:
        print("El servidor LA FILA no respondió después de 3 intentos.")


if __name__ == "__main__":
    main()
