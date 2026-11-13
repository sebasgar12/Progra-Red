"""
Unidad II - Ejercicio 5: LA FILA tolerante a fallos (extensión de Práctica 6)
- TCP (puerto 5000): recibe 'TURNO>apodo\n' y responde 'turno>N\n' sin repetir números.
- UDP (puerto 5001): recibe 'CUANTOS' y responde 'van>N\n'.
- Protege el contador compartido con threading.Lock.
- Registra en consola desconexiones abruptas, mensajes fuera de protocolo
  (distintos de 'TURNO>apodo') y bytes que no son UTF-8 válido sin caer jamás.
"""

import socket
import threading

HOST = "0.0.0.0"
PUERTO_TCP = 5000
PUERTO_UDP = 5001

contador_turnos = 0
candado = threading.Lock()


def atender_cliente(conexion, direccion):
    """Atiende a un cliente TCP tolerando fallos de red, codificación y protocolo."""
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
                            print(f"[PROTOCOLO] {direccion} envió TURNO> sin apodo.")
                            conexion.sendall("ERROR>apodo requerido\n".encode("utf-8"))
                    else:
                        print(f"[PROTOCOLO] {direccion} envió mensaje inválido: {linea!r}")
                        conexion.sendall("ERROR>formato esperado: TURNO>apodo\n".encode("utf-8"))

    except ConnectionResetError:
        print(f"[ERROR RED] {direccion} cerró la conexión abruptamente (ConnectionResetError).")
    except BrokenPipeError:
        print(f"[ERROR RED] Tubería rota al enviar respuesta a {direccion} (BrokenPipeError).")
    except UnicodeDecodeError:
        print(f"[ERROR CODIFICACIÓN] {direccion} envió bytes que no son UTF-8 válido.")
    except OSError as error:
        print(f"[ERROR SOCKET] Problema de red con {direccion}: {error}")
    finally:
        print(f"[TCP CIERRE] Conexión cerrada: {direccion}")


def servidor_udp():
    """Hilo dedicado a responder consultas UDP 'CUANTOS' en el puerto 5001."""
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
        try:
            datos, direccion = sock_udp.recvfrom(1024)
            mensaje = datos.decode("utf-8").strip()

            if mensaje == "CUANTOS":
                with candado:
                    total = contador_turnos
                sock_udp.sendto(f"van>{total}\n".encode("utf-8"), direccion)
                print(f"[UDP CONSULTA] {direccion} -> van>{total}")
            else:
                print(f"[UDP PROTOCOLO] {direccion} envió datagrama inválido: {mensaje!r}")
                sock_udp.sendto("ERROR>comando esperado: CUANTOS\n".encode("utf-8"), direccion)
        except UnicodeDecodeError:
            print("[UDP ERROR] Datagrama recibido con bytes UTF-8 inválidos.")
        except OSError as error:
            print(f"[UDP ERROR] Error de socket UDP: {error}")


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
    print(f"[TCP LA FILA] Escuchando turnos en {HOST}:{PUERTO_TCP}...")

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
