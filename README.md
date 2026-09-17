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

