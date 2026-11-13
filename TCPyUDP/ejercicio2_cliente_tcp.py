"""
Ejercicio 2: Cliente TCP
- Se conecta al servidor TCP del Ejercicio 1 en el puerto 5000.
- Envía tres mensajes (hola, redes, adios) terminados en '\n'.
- Muestra la respuesta del servidor a cada mensaje.
"""

import socket

SERVIDOR = ("127.0.0.1", 5000)
MENSAJES = ["hola", "redes", "adios"]


def main():
    conexion = socket.create_connection(SERVIDOR)
    print(f"[CLIENTE TCP] Conectado a {SERVIDOR}")
    buffer = b""

    for mensaje in MENSAJES:
        conexion.sendall((mensaje + "\n").encode("utf-8"))
        print(f"Enviado: {mensaje}")

        while b"\n" not in buffer:
            datos = conexion.recv(1024)
            if not datos:
                break
            buffer += datos

        if b"\n" in buffer:
            linea_bytes, buffer = buffer.split(b"\n", 1)
            respuesta = linea_bytes.decode("utf-8")
            print(f"Respuesta: {respuesta}")

    conexion.close()
    print("[CLIENTE TCP] Conexión cerrada.")


if __name__ == "__main__":
    main()
