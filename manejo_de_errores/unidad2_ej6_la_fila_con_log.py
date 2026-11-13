"""
Unidad II - Ejercicio 6 (Desafío): LA FILA con registro de errores en archivo
- Extiende el servidor LA FILA del Ejercicio 5 escribiendo cada error en un
  archivo de texto ('errores_la_fila.log') con marca de tiempo, dirección del
  cliente y descripción:
  2026-10-06 10:32:15 (187.141.12.9, 51020) conexión reiniciada por el cliente
- Protege la escritura del archivo con el mismo threading.Lock del contador
  para evitar líneas entrelazadas o incompletas entre hilos concurrentes.
"""

import socket
import threading
import time

HOST = "0.0.0.0"
PUERTO_TCP = 5000
PUERTO_UDP = 5001
ARCHIVO_LOG = "errores_la_fila.log"

contador_turnos = 0
candado = threading.Lock()


def registrar_error(direccion, descripcion):
    """Escribe una línea completa de error en ARCHIVO_LOG de forma segura entre hilos."""
    marca_tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
    dir_formateada = f"({direccion[0]}, {direccion[1]})"
    linea_log = f"{marca_tiempo} {dir_formateada} {descripcion}\n"

    with candado:
        with open(ARCHIVO_LOG, mode="a", encoding="utf-8") as archivo:
            archivo.write(linea_log)

    print(f"[LOG] {linea_log.strip()}")


def atender_cliente(conexion, direccion):
    """Atiende a un cliente TCP y registra cualquier fallo en consola y archivo."""
    global contador_turnos
    buffer = b""
    print(f"[TCP CONEXIÓN] Cliente conectado desde {direccion}")

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

                    if linea.startswith("TURNO>"):
                        apodo = linea[len("TURNO>"):].strip()
                        if apodo:
                            with candado:
                                contador_turnos += 1
                                turno = contador_turnos
                            respuesta = f"turno>{turno}\n"
                            conexion.sendall(respuesta.encode("utf-8"))
                            print(f"[TCP TURNO] {direccion} ({apodo}) -> turno>{turno}")
                        else:
                            registrar_error(direccion, "mensaje fuera de protocolo: TURNO> sin apodo")
                            conexion.sendall("ERROR>apodo requerido\n".encode("utf-8"))
                    else:
                        registrar_error(direccion, f"mensaje fuera de protocolo: {linea!r}")
                        conexion.sendall("ERROR>formato esperado: TURNO>apodo\n".encode("utf-8"))

    except ConnectionResetError:
        registrar_error(direccion, "conexión reiniciada por el cliente")
    except BrokenPipeError:
        registrar_error(direccion, "tubería rota al intentar enviar datos al cliente")
    except UnicodeDecodeError:
        registrar_error(direccion, "datos recibidos no son UTF-8 válido")
    except OSError as error:
        registrar_error(direccion, f"error de socket: {error}")
    finally:
        print(f"[TCP CIERRE] Conexión cerrada: {direccion}")


def servidor_udp():
    """Hilo dedicado a responder consultas UDP 'CUANTOS' y registrar fallos."""
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock_udp.bind((HOST, PUERTO_UDP))
    except OSError:
        print(f"[ERROR UDP] El puerto {PUERTO_UDP} está ocupado.")
        sock_udp.close()
        return

    print(f"[UDP LA FILA] Escuchando consultas en {HOST}:{PUERTO_UDP}...")

    while True:
        direccion = ("desconocida", 0)
        try:
            datos, direccion = sock_udp.recvfrom(1024)
            mensaje = datos.decode("utf-8").strip()

            if mensaje == "CUANTOS":
                with candado:
                    total = contador_turnos
                sock_udp.sendto(f"van>{total}\n".encode("utf-8"), direccion)
                print(f"[UDP CONSULTA] {direccion} -> van>{total}")
            else:
                registrar_error(direccion, f"datagrama UDP fuera de protocolo: {mensaje!r}")
                sock_udp.sendto("ERROR>comando esperado: CUANTOS\n".encode("utf-8"), direccion)
        except UnicodeDecodeError:
            registrar_error(direccion, "datagrama UDP con bytes UTF-8 inválidos")
        except OSError as error:
            registrar_error(direccion, f"error de socket UDP: {error}")


def main():
    hilo_udp = threading.Thread(target=servidor_udp, daemon=True)
    hilo_udp.start()

    servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor_tcp.bind((HOST, PUERTO_TCP))
    except OSError:
        print(f"[ERROR TCP] El puerto {PUERTO_TCP} está ocupado por otro proceso.")
        servidor_tcp.close()
        return

    servidor_tcp.listen()
    print(f"[TCP LA FILA + LOG] Escuchando en {HOST}:{PUERTO_TCP} (log: {ARCHIVO_LOG})...")

    try:
        while True:
            conexion, direccion = servidor_tcp.accept()
            hilo = threading.Thread(
                target=atender_cliente,
                args=(conexion, direccion),
                daemon=True,
            )
            hilo.start()
    except KeyboardInterrupt:
        print("\n[LA FILA] Servidor detenido por el usuario.")
    finally:
        servidor_tcp.close()


if __name__ == "__main__":
    main()
