"""
Modelos de datos (Pydantic).

Si vienes de Java: piensa en cada clase de aquí como un DTO o un POJO con
validaciones de Bean Validation (@NotNull, @Size, etc), pero declarativo.
FastAPI usa estas clases para:
  1. Validar automáticamente lo que llega en el body del request.
  2. Generar la documentación interactiva (Swagger) sola.
  3. Serializar la respuesta que se manda de vuelta al cliente.
"""

from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TipoImprevisto(str, Enum):
    """Enum = lista cerrada de valores válidos (como un enum de Java)."""
    FALTA_MATERIAL = "falta_material"
    CLIMA = "clima"
    DANO_ESTRUCTURAL = "dano_estructural"
    AUSENCIA_PERSONAL = "ausencia_personal"
    OTRO = "otro"


class ImprevistoCrear(BaseModel):
    """Lo que el cliente (frontend / Swagger / Postman) envía para crear un imprevisto."""

    obra_id: UUID = Field(..., description="ID de la obra a la que pertenece el imprevisto")
    fecha: date = Field(..., description="Fecha en la que ocurrió el imprevisto (YYYY-MM-DD)")
    hubo_retraso: bool = Field(..., description="¿Este imprevisto generó un retraso en la obra?")
    tipo_imprevisto: TipoImprevisto
    descripcion: str = Field(
        ..., min_length=5, max_length=500,
        description="Explicación del motivo, mínimo 5 caracteres"
    )
    horas_retraso: Optional[float] = Field(
        default=None, ge=0, le=24,
        description="Horas de retraso que generó (opcional, solo si hubo_retraso=true)"
    )

    @field_validator("descripcion")
    @classmethod
    def descripcion_no_vacia(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("La descripción no puede estar vacía ni contener solo espacios.")
        return v

    @field_validator("horas_retraso")
    @classmethod
    def horas_coherentes_con_retraso(cls, v, info):
        # Regla de negocio simple: si no hubo retraso, no debería reportar horas.
        hubo_retraso = info.data.get("hubo_retraso")
        if hubo_retraso is False and v not in (None, 0):
            raise ValueError(
                "Si 'hubo_retraso' es falso, no debe reportarse un valor en 'horas_retraso'."
            )
        return v


class ImprevistoActualizar(BaseModel):
    """Campos opcionales para una edición parcial (PATCH)."""

    hubo_retraso: Optional[bool] = None
    tipo_imprevisto: Optional[TipoImprevisto] = None
    descripcion: Optional[str] = Field(default=None, min_length=5, max_length=500)
    horas_retraso: Optional[float] = Field(default=None, ge=0, le=24)


class ImprevistoRespuesta(BaseModel):
    """Lo que la API devuelve al cliente."""

    id: UUID
    obra_id: UUID
    fecha: date
    hubo_retraso: bool
    tipo_imprevisto: TipoImprevisto
    descripcion: str
    horas_retraso: Optional[float]
    creado_en: datetime


class ErrorRespuesta(BaseModel):
    """Formato consistente de error para que el frontend siempre sepa qué esperar."""

    detalle: str
    codigo: str
