"""
Ejercicio 3 (Cliente): Consulta UDP
- Envía el datagrama 'ESTADO' al servidor UDP en el puerto 5001.
- Espera la respuesta a lo más 3 segundos (settimeout(3)).
"""

import socket

SERVIDOR_UDP = ("127.0.0.1", 5001)


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente.settimeout(3)

    try:
        cliente.sendto("ESTADO".encode("utf-8"), SERVIDOR_UDP)
        print(f"[CLIENTE UDP] Consulta 'ESTADO' enviada a {SERVIDOR_UDP}...")

        datos, direccion = cliente.recvfrom(1024)
        respuesta = datos.decode("utf-8")
        print(f"[CLIENTE UDP] Respuesta desde {direccion}: {respuesta}")
    except socket.timeout:
        print("[CLIENTE UDP] Tiempo agotado: no hubo respuesta en 3 segundos.")
    finally:
        cliente.close()


if __name__ == "__main__":
    main()
