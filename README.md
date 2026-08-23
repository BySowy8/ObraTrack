# ObraTrack — HU2: Registro de imprevistos y retrasos diarios

Backend en **FastAPI** + **Supabase** para la Historia de Usuario 2 del Sprint 1.

> Complementa la Bitácora Diaria (HU1): permite marcar si hubo retraso en el
> día y registrar el motivo (falta de material, clima, daño estructural, etc.).

## Estructura del proyecto

```
obratrack-hu2/
├── main.py                    # App de FastAPI + manejo global de errores
├── models.py                  # Esquemas Pydantic (validación de datos)
├── supabase_client.py         # Conexión centralizada a Supabase
├── routers/
│   └── imprevistos.py         # Endpoints de la HU2 (CRUD)
├── sql/
│   └── schema.sql             # Tablas a crear en Supabase
├── tests/
│   └── prueba_manual.py       # Script de verificación manual (DoD)
├── ObraTrack_HU2_Colab.ipynb  # Notebook para correr todo en Google Colab
├── requirements.txt
├── .env.example
└── .gitignore
```

## 1. Preparar Supabase

1. Entra a tu proyecto de Supabase → **SQL Editor** → **New query**.
2. Pega y ejecuta el contenido de `sql/schema.sql`.
3. Esto crea la tabla `obras` (con una fila de prueba) y la tabla
   `imprevistos` con sus validaciones (`CHECK constraints`), índices y
   Row Level Security básico.
4. Ve a **Table Editor → obras**, copia el `id` de la fila de prueba —
   lo vas a necesitar para probar la API.
5. Ve a **Project Settings → API** y copia `Project URL` y `anon public key`.

## 2. Configurar variables de entorno

Copia `.env.example` como `.env` y llena tus valores:

```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-api-key-aqui
```

**Nunca subas el archivo `.env` real a GitHub** (ya está en `.gitignore`).

## 3. Correr localmente (opcional, si no usas Colab)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Abre http://127.0.0.1:8000/docs para la documentación interactiva (Swagger).

## 4. Correr en Google Colab

Abre `ObraTrack_HU2_Colab.ipynb` en Colab y sigue las celdas en orden:
1. Clona tu repo.
2. Instala dependencias.
3. Define `SUPABASE_URL` y `SUPABASE_KEY`.
4. Configura tu authtoken de [ngrok](https://ngrok.com) (gratis).
5. Levanta el servidor y obtén una URL pública (`https://xxxx.ngrok.app`).
6. Abre `/docs` en esa URL para probar todo desde el navegador.

## 5. Endpoints de la HU2

| Método | Ruta                     | Qué hace                                   |
|--------|--------------------------|---------------------------------------------|
| POST   | `/imprevistos`           | Registrar un nuevo imprevisto/retraso        |
| GET    | `/imprevistos`           | Listar, con filtros: `obra_id`, `fecha_inicio`, `fecha_fin`, `solo_con_retraso` |
| GET    | `/imprevistos/{id}`      | Ver el detalle de uno                        |
| PATCH  | `/imprevistos/{id}`      | Corregir un registro existente               |
| DELETE | `/imprevistos/{id}`      | Eliminar un registro creado por error         |

Ejemplo de body para `POST /imprevistos`:

```json
{
  "obra_id": "PEGA-AQUI-EL-UUID-DE-LA-OBRA",
  "fecha": "2026-08-20",
  "hubo_retraso": true,
  "tipo_imprevisto": "falta_material",
  "descripcion": "No llegó el cemento a tiempo, proveedor confirmó envío para mañana.",
  "horas_retraso": 3.5
}
```

## 6. Cómo cumple el Definition of Done del Sprint 1

- **Persistencia real**: los registros se guardan en Supabase (Postgres), no en memoria.
- **Manejo de errores visible**: campos vacíos o inválidos devuelven un
  JSON con `detalle` y `errores` en español (ver `main.py` y
  `routers/imprevistos.py`), no una traza técnica cruda.
- **Pruebas funcionales**: `tests/prueba_manual.py` recorre los flujos
  (crear válido, crear inválido, listar, consultar, editar, eliminar,
  buscar uno inexistente) y un compañero puede correrlo y confirmar que
  todo se comporta como se espera.

## 7. Flujo de trabajo en GitHub (Pull Request)

El DoD exige que el código llegue por PR revisado por otro integrante:

```bash
git checkout -b feature/hu2-registro-imprevistos
git add .
git commit -m "HU2: registro de imprevistos y retrasos diarios"
git push origin feature/hu2-registro-imprevistos
```

Luego, en GitHub:
1. Abre un **Pull Request** de tu rama hacia `main`.
2. Asigna como *reviewer* a otro integrante del equipo.
3. Solo se hace merge cuando alguien más aprueba el PR.

## 8. Siguientes pasos sugeridos

- Cuando HU1 tenga lista su propia tabla `obras` con más campos, reemplaza
  el stub de `sql/schema.sql` por la tabla real de tu compañero (mismo
  nombre `obras` y columna `id` de tipo `uuid` para que la FK siga funcionando).
- La HU3 (Consulta y Filtrado del Historial) puede reutilizar directamente
  el endpoint `GET /imprevistos` — ya soporta filtros por fecha y por obra.
