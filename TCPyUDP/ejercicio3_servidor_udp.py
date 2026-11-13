"""
Ejercicio 3 (Servidor): Consulta UDP
- Escucha datagramas UDP en el puerto 5001.
- Responde 'servidor activo' cuando recibe el datagrama 'ESTADO'.
"""

import socket

HOST = "0.0.0.0"
PUERTO = 5001


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PUERTO))
    print(f"[UDP] Servidor escuchando en {HOST}:{PUERTO}...")

    try:
        while True:
            datos, direccion = servidor.recvfrom(1024)
            mensaje = datos.decode("utf-8").strip()
            print(f"[{direccion}] Datagrama recibido: {mensaje}")

            if mensaje == "ESTADO":
                servidor.sendto("servidor activo".encode("utf-8"), direccion)
    except KeyboardInterrupt:
        print("\n[UDP] Servidor detenido.")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
