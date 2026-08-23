"""
Punto de entrada de la aplicación ObraTrack (backend HU2).

Correr localmente:
    uvicorn main:app --reload

Correr en Google Colab:
    ver instrucciones en README.md (usamos pyngrok para exponer el puerto).
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import imprevistos

app = FastAPI(
    title="ObraTrack API",
    description="Backend de ObraTrack - HU2: Registro de imprevistos y retrasos diarios",
    version="0.1.0",
)

# CORS abierto para el Sprint 1 (mientras no hay dominio de frontend definido).
# Antes de producción, restringir a los orígenes reales.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(imprevistos.router)


@app.exception_handler(RequestValidationError)
async def manejar_error_validacion(request: Request, exc: RequestValidationError):
    """
    Convierte los errores de validación de Pydantic (422 por defecto, con
    un formato técnico) en un mensaje amigable en español. Esto es lo que
    cumple "Manejo de Errores Visible" cuando falta un campo obligatorio
    o llega un tipo de dato inválido.
    """
    errores_legibles = []
    for error in exc.errors():
        campo = ".".join(str(parte) for parte in error["loc"] if parte != "body")
        errores_legibles.append(f"{campo}: {error['msg']}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detalle": "Hay campos inválidos o faltantes en tu solicitud.",
            "errores": errores_legibles,
        },
    )


@app.get("/", tags=["Salud"])
def estado() -> dict:
    """Endpoint simple para confirmar que la API está viva."""
    return {"estado": "ok", "servicio": "ObraTrack API"}
