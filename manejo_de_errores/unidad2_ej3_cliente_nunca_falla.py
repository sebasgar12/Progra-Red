"""
Unidad II - Ejercicio 3: Cliente que nunca falla
- Solicita al usuario la IP o host del servidor TCP.
- Maneja con mensajes claros y sin tracebacks:
  1. IP o nombre inválido / no resoluble (socket.gaierror).
  2. Servidor apagado / conexión rechazada (ConnectionRefusedError).
  3. Respuesta que nunca llega / tiempo agotado (TimeoutError).
  4. Desconexión del servidor a media conversación (ConnectionResetError / BrokenPipeError).
- Termina con sys.exit(1) ante cualquier fallo.
"""

import socket
import sys

PUERTO = 5000
MENSAJES = ["hola", "redes", "adios"]


def main():
    ip_servidor = input("Ingrese la IP o nombre del servidor: ").strip()
    if not ip_servidor:
        print("Error: no se ingresó ninguna dirección IP o host.")
        sys.exit(1)

    try:
        conexion = socket.create_connection((ip_servidor, PUERTO), timeout=5)
    except socket.gaierror:
        print(f"Error: la dirección '{ip_servidor}' no es válida o no se puede resolver.")
        sys.exit(1)
    except ConnectionRefusedError:
        print(f"Error: el servidor en {ip_servidor}:{PUERTO} está apagado o rechaza conexiones.")
        sys.exit(1)
    except TimeoutError:
        print(f"Error: tiempo de espera agotado al intentar conectar con {ip_servidor}:{PUERTO}.")
        sys.exit(1)
    except OSError as error:
        print(f"Error de red al conectar con {ip_servidor}:{PUERTO}: {error}")
        sys.exit(1)

    with conexion:
        conexion.settimeout(5)
        buffer = b""
        print(f"Conectado a {ip_servidor}:{PUERTO}")

        for mensaje in MENSAJES:
            try:
                conexion.sendall((mensaje + "\n").encode("utf-8"))
                print(f"Enviado: {mensaje}")

                while b"\n" not in buffer:
                    datos = conexion.recv(1024)
                    if not datos:
                        raise ConnectionResetError("El servidor cerró la conexión inesperadamente.")
                    buffer += datos

                linea_bytes, buffer = buffer.split(b"\n", 1)
                respuesta = linea_bytes.decode("utf-8")
                print(f"Servidor responde: {respuesta}")

            except TimeoutError:
                print("Error: la respuesta del servidor nunca llegó (tiempo agotado).")
                sys.exit(1)
            except (ConnectionResetError, BrokenPipeError):
                print("Error: el servidor se desconectó a media conversación.")
                sys.exit(1)
            except UnicodeDecodeError:
                print("Error: el servidor envió datos con codificación inválida.")
                sys.exit(1)
            except OSError as error:
                print(f"Error de comunicación durante la sesión: {error}")
                sys.exit(1)

    print("Conversación finalizada correctamente.")


if __name__ == "__main__":
    main()
