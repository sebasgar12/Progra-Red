import threading
import socket

def atender_cliente(conexion, direccion):
    with conexion:
        bufer = ""
        while True:
            datos = conexion.recv(1024)
            if not datos:
                break
            bufer += datos.decode('utf-8')
            while '\n' in bufer:
                linea, bufer = bufer.split('\n', 1)
                conexion.sendall((linea + '\n').encode('utf-8'))
    print(f"Conexión cerrada desde {direccion}")

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", 5000))
    servidor.listen()
    print("Servidor escuchando en el puerto 5000...")
    while True:
        conexion, direccion = servidor.accept()
        hilo = threading.Thread(target=atender_cliente, args=(conexion, direccion), daemon=True)
        hilo.start()
main()