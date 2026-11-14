"""
Práctica 8 - Cliente HTTP en Python para consumir servidor_bitacora.py
Archivo: cliente_bitacora.py

Recorre el ciclo completo CRUD (POST, GET con filtros combinados, PATCH, PUT,
DELETE), valida manejo de códigos 400/404 y consulta la auditoría (/contadores
y /logs).
"""

import sys
import requests

BASE = "http://localhost:8001"


def main():
    try:
        # 1. Consultar información raíz del servicio
        r = requests.get(f"{BASE}/", timeout=10)
        print("GET / ->", r.status_code, r.json())

        # 2. Crear incidencias (POST -> 201)
        r1 = requests.post(
            f"{BASE}/incidencias",
            json={"tipo": "alerta", "descripcion": "Escaneo de puertos"},
            timeout=10,
        )
        print("POST /incidencias (1) ->", r1.status_code, r1.json())
        inc1 = r1.json()

        r2 = requests.post(
            f"{BASE}/incidencias",
            json={
                "tipo": "vulnerabilidad",
                "descripcion": "SSH con contraseña débil",
                "estado": "en_proceso",
            },
            timeout=10,
        )
        print("POST /incidencias (2) ->", r2.status_code, r2.json())
        inc2 = r2.json()

        # 3. Probar validación de vocabulario controlado en POST (400)
        r_err_estado = requests.post(
            f"{BASE}/incidencias",
            json={"tipo": "alerta", "descripcion": "Prueba", "estado": "pendiente"},
            timeout=10,
        )
        print("POST estado inválido ->", r_err_estado.status_code, r_err_estado.json())

        # 4. Consultar todas y con filtros combinados (Ejercicio 5)
        r_todas = requests.get(f"{BASE}/incidencias", timeout=10)
        print("GET /incidencias -> total:", len(r_todas.json()))

        r_tipo = requests.get(f"{BASE}/incidencias", params={"tipo": "alerta"}, timeout=10)
        print("GET ?tipo=alerta ->", r_tipo.json())

        r_comb = requests.get(
            f"{BASE}/incidencias",
            params={"tipo": "alerta", "estado": "abierta"},
            timeout=10,
        )
        print("GET ?tipo=alerta&estado=abierta ->", r_comb.json())

        # 5. Modificar parcialmente con PATCH -> 200
        r_patch = requests.patch(
            f"{BASE}/incidencias/{inc1['id']}",
            json={"estado": "resuelta"},
            timeout=10,
        )
        print(f"PATCH /incidencias/{inc1['id']} ->", r_patch.status_code, r_patch.json())

        # Validar filtro combinado tras cambio de estado (ya no debe salir como abierta)
        r_comb2 = requests.get(
            f"{BASE}/incidencias",
            params={"tipo": "alerta", "estado": "abierta"},
            timeout=10,
        )
        print("GET ?tipo=alerta&estado=abierta tras PATCH ->", r_comb2.json())

        # 6. Reemplazo completo con PUT -> 200 (Ejercicio 4: reinicia estado a 'abierta')
        r_put = requests.put(
            f"{BASE}/incidencias/{inc1['id']}",
            json={"tipo": "incidente", "descripcion": "Escaneo de puertos confirmado"},
            timeout=10,
        )
        print(f"PUT /incidencias/{inc1['id']} ->", r_put.status_code, r_put.json())

        # 7. Consultar incidencia inexistente -> 404
        r_404 = requests.get(f"{BASE}/incidencias/999", timeout=10)
        if r_404.status_code == 404:
            print("GET /incidencias/999 -> 404:", r_404.json()["error"])

        # 8. Eliminar la segunda incidencia con DELETE -> 204
        r_del = requests.delete(f"{BASE}/incidencias/{inc2['id']}", timeout=10)
        print(f"DELETE /incidencias/{inc2['id']} ->", r_del.status_code)

        # 9. Consultar auditoría del servidor (/contadores y /logs)
        print("GET /contadores ->", requests.get(f"{BASE}/contadores", timeout=10).json())
        print("GET /logs ->", len(requests.get(f"{BASE}/logs", timeout=10).json()), "registros")

    except requests.exceptions.ConnectionError:
        print(f"Error: no se pudo conectar con {BASE}. Verifica que servidor_bitacora.py esté ejecutándose.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: tiempo de espera agotado al comunicarse con el servidor.")
        sys.exit(1)


if __name__ == "__main__":
    main()
