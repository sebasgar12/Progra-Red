import socket
def iniciar_cliente():
    HOST = '172.20.10.13'  # Cambiar por la IP del defensor si está en otra máquina
    PORT = 5050
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))
    print("[ATACANTE] Conectado con el defensor. ¡Comienza el ataque!")
    try:
        while True:
            # Ingresar coordenadade ataque (request)
            coordenada = input("Ingresa coordenada de ataque (ej. A1) o 'salir': ")
            if coordenada.lower() == 'salir':
                break
            # Enviar la coordenada codificada
            cliente.send(coordenada.encode('utf-8'))
            # Recibir la respuesta del servidor (response)
            respuesta = cliente.recv(1024).decode('utf-8')
            print(f"[RESPUESTA DEL DEFENSOR]: {respuesta}")
    finally:
        cliente.close()
if __name__ == "__main__":
    iniciar_cliente()

 