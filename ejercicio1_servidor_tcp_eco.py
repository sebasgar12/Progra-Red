"""
Ejercicio 1: Servidor TCP de eco
- Escucha en el puerto 5000.
- Reenvía al cliente cada línea recibida (framing por salto de línea '\n').
- Permite reutilizar el puerto tras reiniciarlo (SO_REUSEADDR).
- Codificación: UTF-8.
"""

import socket

HOST = "0.0.0.0"
PUERTO = 5000


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PUERTO))
    servidor.listen()
    print(f"[TCP ECO] Servidor escuchando en {HOST}:{PUERTO}...")

    try:
        while True:
            conexion, direccion = servidor.accept()
            print(f"[CONEXIÓN] Cliente conectado desde {direccion}")
            buffer = b""

            while True:
                datos = conexion.recv(1024)
                if not datos:
                    # recv() vacío indica que el cliente cerró la conexión
                    print(f"[DESCONEXIÓN] Cliente {direccion} cerró la conexión.")
                    break

                buffer += datos
                while b"\n" in buffer:
                    linea_bytes, buffer = buffer.split(b"\n", 1)
                    mensaje = linea_bytes.decode("utf-8")
                    print(f"[{direccion}] Recibido: {mensaje}")
                    respuesta = (mensaje + "\n").encode("utf-8")
                    conexion.sendall(respuesta)

            conexion.close()
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Deteniendo servidor...")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
