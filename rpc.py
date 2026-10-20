from xmlrpc.server import SimpleXMLRPCServer
import threading

class SistemaLaFila:
    def __init__(self):
        self.lock = threading.Lock()
        self.total_turnos = 0

    def tomar_turno(self, apodo):
        # Protegemos la sección crítica con el Lock
        with self.lock:
            self.total_turnos += 1
            turno_asignado = self.total_turnos
            
        print(f"Asignando el turno #{turno_asignado} a '{apodo}'.")
        return turno_asignado

    def cuantos_van(self):
        # Devuelve el total de turnos asignados
        return self.total_turnos

def iniciar_servidor():
    # Creamos el servidor en localhost, puerto 8000
    servidor = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    
    # Registramos la instancia con nuestras dos funciones
    servidor.register_instance(SistemaLaFila())
    
    print("Servidor 'LA FILA' iniciado en http://localhost:8000")
    print("Esperando clientes (Presiona Ctrl+C para salir)...")
    
    # El servidor se queda escuchando peticiones
    servidor.serve_forever()

if __name__ == "__main__":
    iniciar_servidor()
