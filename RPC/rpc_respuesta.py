import xmlrpc.client

def iniciar_cliente():
    # Nos conectamos al servidor usando XML-RPC
    servidor = xmlrpc.client.ServerProxy("http://localhost:8000/")
    
    # Se pide el apodo por teclado
    apodo = input("¡Bienvenido a LA FILA!\nPor favor, ingresa tu apodo: ")
    
    try:
        # Llamamos a la primera función: tomar_turno
        mi_turno = servidor.tomar_turno(apodo)
        print(f"\n¡Éxito, {apodo}! Tu número de turno es: {mi_turno}")
        
        # Llamamos a la segunda función: cuantos_van
        total = servidor.cuantos_van()
        print(f"Dato curioso: Hasta ahora se han asignado {total} turnos en total.")
        
    except ConnectionRefusedError:
        print("\nError: No se pudo conectar al servidor. Asegúrate de que 'servidor.py' esté ejecutándose.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")

if __name__ == "__main__":
    iniciar_cliente()