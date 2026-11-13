"""
Ejercicio 4: Servidor multicliente con hilos
- Convierte el servidor TCP de eco del Ejercicio 1 en multicliente.
- Cada conexión aceptada se atiende en su propio hilo (daemon=True).
- El hilo principal únicamente acepta nuevas conexiones.
"""

import socket
import threading

HOST = "0.0.0.0"
PUERTO = 5000


def atender_cliente(conexion, direccion):
    print(f"[HILO {threading.current_thread().name}] Atendiendo a {direccion}")
    buffer = b""

    while True:
        datos = conexion.recv(1024)
        if not datos:
            print(f"[DESCONEXIÓN] Cliente {direccion} cerró la conexión.")
            break

        buffer += datos
        while b"\n" in buffer:
            linea_bytes, buffer = buffer.split(b"\n", 1)
            mensaje = linea_bytes.decode("utf-8")
            print(f"[{direccion}] Eco: {mensaje}")
            conexion.sendall((mensaje + "\n").encode("utf-8"))

    conexion.close()


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PUERTO))
    servidor.listen()
    print(f"[TCP MULTICLIENTE] Servidor escuchando en {HOST}:{PUERTO}...")

    try:
        while True:
            conexion, direccion = servidor.accept()
            hilo = threading.Thread(
                target=atender_cliente,
                args=(conexion, direccion),
                daemon=True,
            )
            hilo.start()
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Deteniendo servidor multicliente...")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
