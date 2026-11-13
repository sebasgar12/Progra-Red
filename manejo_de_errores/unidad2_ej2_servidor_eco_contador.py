"""
Unidad II - Ejercicio 2: Servidor de eco con contador por cliente
- Extiende el servidor TCP robusto (Código 4) para numerar los mensajes
  de cada cliente de forma independiente: '1>hola\n', '2>otro\n', etc.
- El contador es una variable local dentro de atender_cliente.
"""

import socket
import threading

HOST = "0.0.0.0"
PUERTO = 5000


def atender_cliente(conexion, direccion):
    """Atiende a un cliente manteniendo su propio contador de mensajes."""
    contador = 0
    buffer = b""
    print(f"[CONEXIÓN] Cliente conectado desde {direccion}")

    try:
        with conexion:
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break

                buffer += datos
                while b"\n" in buffer:
                    linea_bytes, buffer = buffer.split(b"\n", 1)
                    linea = linea_bytes.decode("utf-8").rstrip("\r")
                    contador += 1
                    respuesta = f"{contador}>{linea}\n"
                    print(f"[{direccion}] ({contador}) {linea}")
                    conexion.sendall(respuesta.encode("utf-8"))

    except ConnectionResetError:
        print(f"[ALERTA] El cliente {direccion} se desconectó abruptamente.")
    except BrokenPipeError:
        print(f"[ALERTA] No se pudo enviar respuesta a {direccion} (conexión cerrada).")
    except UnicodeDecodeError:
        print(f"[ALERTA] El cliente {direccion} envió datos que no son UTF-8 válido.")
    finally:
        print(f"[CIERRE] Conexión cerrada con {direccion} (total mensajes: {contador})")


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((HOST, PUERTO))
    except OSError:
        print(f"[ERROR] El puerto {PUERTO} está ocupado por otro proceso.")
        servidor.close()
        return

    servidor.listen()
    print(f"[SERVIDOR ECO CONTADOR] Escuchando en {HOST}:{PUERTO}...")

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
        print("\n[SERVIDOR] Deteniendo servidor...")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
