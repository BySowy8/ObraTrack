"""
Script de verificación manual de los flujos de la HU2.

Esto NO reemplaza pruebas automatizadas (pytest), pero cumple con el
requisito del DoD de "Pruebas Funcionales: verificación manual exitosa de
los flujos de usuario por parte de un compañero de equipo": corre este
script, revisa la salida en consola, y que un compañero confirme que cada
paso se comporta como se espera.

Uso:
    1. Ten la API corriendo (localmente con `uvicorn main:app --reload`,
       o en Colab con la URL de ngrok).
    2. Ajusta BASE_URL abajo.
    3. Ajusta OBRA_ID_PRUEBA con el id real de la fila de prueba en
       Supabase (tabla "obras").
    4. Ejecuta: python tests/prueba_manual.py
"""

import requests

BASE_URL = "http://127.0.0.1:8000"  # cámbialo por tu URL de ngrok si corres en Colab
OBRA_ID_PRUEBA = "PEGA_AQUI_EL_ID_DE_LA_OBRA_DE_PRUEBA"


def paso(titulo: str) -> None:
    print(f"\n{'=' * 60}\n{titulo}\n{'=' * 60}")


def main() -> None:
    paso("1. Verificar que la API está viva")
    respuesta = requests.get(f"{BASE_URL}/")
    print(respuesta.status_code, respuesta.json())
    assert respuesta.status_code == 200

    paso("2. Crear un imprevisto válido (flujo feliz)")
    payload_valido = {
        "obra_id": OBRA_ID_PRUEBA,
        "fecha": "2026-08-20",
        "hubo_retraso": True,
        "tipo_imprevisto": "falta_material",
        "descripcion": "No llegó el cemento a tiempo, proveedor confirmó envío para mañana.",
        "horas_retraso": 3.5,
    }
    respuesta = requests.post(f"{BASE_URL}/imprevistos", json=payload_valido)
    print(respuesta.status_code, respuesta.json())
    assert respuesta.status_code == 201
    imprevisto_creado = respuesta.json()
    imprevisto_id = imprevisto_creado["id"]

    paso("3. Intentar crear un imprevisto con descripción vacía (debe fallar con error claro)")
    payload_invalido = {**payload_valido, "descripcion": "  "}
    respuesta = requests.post(f"{BASE_URL}/imprevistos", json=payload_invalido)
    print(respuesta.status_code, respuesta.json())
    assert respuesta.status_code == 422

    paso("4. Intentar crear un imprevisto sin campos obligatorios (debe fallar con error claro)")
    respuesta = requests.post(f"{BASE_URL}/imprevistos", json={"fecha": "2026-08-20"})
    print(respuesta.status_code, respuesta.json())
    assert respuesta.status_code == 422

    paso("5. Listar imprevistos de la obra de prueba")
    respuesta = requests.get(f"{BASE_URL}/imprevistos", params={"obra_id": OBRA_ID_PRUEBA})
    print(respuesta.status_code, respuesta.json())
    assert respuesta.status_code == 200
    assert any(item["id"] == imprevisto_id for item in respuesta.json())

    paso("6. Consultar el detalle del imprevisto creado")
    respuesta = requests.get(f"{BASE_URL}/imprevistos/{imprevisto_id}")
    print(respuesta.status_code, respuesta.json())
    assert respuesta.status_code == 200

    paso("7. Consultar un imprevisto que no existe (debe devolver 404 claro)")
    respuesta = requests.get(f"{BASE_URL}/imprevistos/00000000-0000-0000-0000-000000000000")
    print(respuesta.status_code, respuesta.json())
    assert respuesta.status_code == 404

    paso("8. Corregir el imprevisto creado (PATCH)")
    respuesta = requests.patch(
        f"{BASE_URL}/imprevistos/{imprevisto_id}",
        json={"descripcion": "Actualizado: el cemento llegó con 3.5h de retraso confirmado."},
    )
    print(respuesta.status_code, respuesta.json())
    assert respuesta.status_code == 200

    paso("9. Eliminar el imprevisto de prueba (limpieza)")
    respuesta = requests.delete(f"{BASE_URL}/imprevistos/{imprevisto_id}")
    print(respuesta.status_code)
    assert respuesta.status_code == 204

    print("\n✅ Todos los flujos probados manualmente pasaron correctamente.")


if __name__ == "__main__":
    main()
