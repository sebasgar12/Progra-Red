"""
Ejercicio 5 (a): Cliente TCP endurecido con manejo de excepciones
- Informa con mensajes claros si:
  1. La dirección IP/host no se puede resolver (socket.gaierror).
  2. El servidor está apagado o rechaza la conexión (ConnectionRefusedError).
  3. El servidor se desconecta o reinicia a media conversación
     (ConnectionResetError, BrokenPipeError o cierre inesperado).
"""

import socket
import time

HOST_SERVIDOR = "127.0.0.1"
PUERTO_SERVIDOR = 5000
MENSAJES = ["hola", "redes", "adios"]


def main():
    conexion = None
    try:
        conexion = socket.create_connection((HOST_SERVIDOR, PUERTO_SERVIDOR), timeout=5)
        print(f"[CLIENTE TCP] Conectado a {HOST_SERVIDOR}:{PUERTO_SERVIDOR}")
        buffer = b""

        for mensaje in MENSAJES:
            conexion.sendall((mensaje + "\n").encode("utf-8"))
            print(f"Enviado: {mensaje}")

            while b"\n" not in buffer:
                datos = conexion.recv(1024)
                if not datos:
                    raise ConnectionResetError("El servidor cerró la conexión inesperadamente.")
                buffer += datos

            linea_bytes, buffer = buffer.split(b"\n", 1)
            respuesta = linea_bytes.decode("utf-8")
            print(f"Respuesta: {respuesta}")
            time.sleep(0.5)

    except socket.gaierror:
        print(f"[ERROR DE RED] No se pudo resolver la dirección '{HOST_SERVIDOR}'. Verifique la IP o dominio.")
    except ConnectionRefusedError:
        print(f"[ERROR DE CONEXIÓN] El servidor en {HOST_SERVIDOR}:{PUERTO_SERVIDOR} está apagado o no acepta conexiones.")
    except (ConnectionResetError, BrokenPipeError):
        print("[ERROR DE CONVERSACIÓN] El servidor se desconectó abruptamente a media conversación.")
    except socket.timeout:
        print("[ERROR DE TIEMPO] Tiempo de espera agotado al comunicarse con el servidor.")
    except OSError as error:
        print(f"[ERROR DE SOCKET] Ocurrió un problema de red: {error}")
    finally:
        if conexion is not None:
            conexion.close()
            print("[CLIENTE TCP] Socket cerrado.")


if __name__ == "__main__":
    main()
