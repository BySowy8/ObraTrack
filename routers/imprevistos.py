"""
Endpoints de la Historia de Usuario 2:
"Registro de imprevistos y retrasos diarios".

Si vienes de Java/Spring: piensa en este archivo como un @RestController,
y cada función decorada con @router.get/@router.post como un método de
ese controlador.
"""

from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from postgrest.exceptions import APIError

from models import ImprevistoActualizar, ImprevistoCrear, ImprevistoRespuesta
from supabase_client import ConfiguracionSupabaseError, obtener_cliente

router = APIRouter(prefix="/imprevistos", tags=["Imprevistos"])

TABLA = "imprevistos"


def _manejar_error_supabase(error: Exception) -> None:
    """
    Traduce errores técnicos de Supabase/Postgres a mensajes claros y
    consistentes. Cumple el requisito de "Manejo de Errores Visible":
    el usuario nunca debería ver una traza de Python cruda.
    """
    if isinstance(error, ConfiguracionSupabaseError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de configuración del servidor: no se pudo conectar a la base de datos.",
        )
    if isinstance(error, APIError):
        # Ej: violación del CHECK constraint de tipo_imprevisto, FK inválida, etc.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo procesar la solicitud: {error.message}",
        )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Ocurrió un error inesperado al conectar con la base de datos. Intenta de nuevo.",
    )


@router.post(
    "",
    response_model=ImprevistoRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo imprevisto o retraso",
)
def crear_imprevisto(payload: ImprevistoCrear) -> ImprevistoRespuesta:
    try:
        cliente = obtener_cliente()
        datos = payload.model_dump(mode="json")
        respuesta = cliente.table(TABLA).insert(datos).execute()
    except (ConfiguracionSupabaseError, APIError) as error:
        _manejar_error_supabase(error)
    except Exception as error:  # noqa: BLE001 - queremos capturar cualquier fallo de red
        _manejar_error_supabase(error)

    if not respuesta.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="La base de datos no confirmó la creación del registro.",
        )

    return respuesta.data[0]


@router.get(
    "",
    response_model=list[ImprevistoRespuesta],
    summary="Listar imprevistos, con filtros opcionales",
)
def listar_imprevistos(
    obra_id: Optional[UUID] = Query(default=None, description="Filtrar por obra"),
    fecha_inicio: Optional[date] = Query(default=None, description="Filtrar desde esta fecha"),
    fecha_fin: Optional[date] = Query(default=None, description="Filtrar hasta esta fecha"),
    solo_con_retraso: Optional[bool] = Query(
        default=None, description="Si es true, solo devuelve imprevistos con hubo_retraso=true"
    ),
) -> list[ImprevistoRespuesta]:
    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'fecha_inicio' no puede ser posterior a 'fecha_fin'.",
        )

    try:
        cliente = obtener_cliente()
        consulta = cliente.table(TABLA).select("*").order("fecha", desc=True)

        if obra_id:
            consulta = consulta.eq("obra_id", str(obra_id))
        if fecha_inicio:
            consulta = consulta.gte("fecha", fecha_inicio.isoformat())
        if fecha_fin:
            consulta = consulta.lte("fecha", fecha_fin.isoformat())
        if solo_con_retraso is not None:
            consulta = consulta.eq("hubo_retraso", solo_con_retraso)

        respuesta = consulta.execute()
    except (ConfiguracionSupabaseError, APIError) as error:
        _manejar_error_supabase(error)
    except Exception as error:  # noqa: BLE001
        _manejar_error_supabase(error)

    return respuesta.data


@router.get(
    "/{imprevisto_id}",
    response_model=ImprevistoRespuesta,
    summary="Obtener el detalle de un imprevisto",
)
def obtener_imprevisto(imprevisto_id: UUID) -> ImprevistoRespuesta:
    try:
        cliente = obtener_cliente()
        respuesta = (
            cliente.table(TABLA).select("*").eq("id", str(imprevisto_id)).execute()
        )
    except (ConfiguracionSupabaseError, APIError) as error:
        _manejar_error_supabase(error)
    except Exception as error:  # noqa: BLE001
        _manejar_error_supabase(error)

    if not respuesta.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un imprevisto con id={imprevisto_id}.",
        )

    return respuesta.data[0]


@router.patch(
    "/{imprevisto_id}",
    response_model=ImprevistoRespuesta,
    summary="Corregir un imprevisto ya registrado",
)
def actualizar_imprevisto(
    imprevisto_id: UUID, payload: ImprevistoActualizar
) -> ImprevistoRespuesta:
    cambios = payload.model_dump(mode="json", exclude_unset=True)
    if not cambios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar.",
        )

    try:
        cliente = obtener_cliente()
        respuesta = (
            cliente.table(TABLA).update(cambios).eq("id", str(imprevisto_id)).execute()
        )
    except (ConfiguracionSupabaseError, APIError) as error:
        _manejar_error_supabase(error)
    except Exception as error:  # noqa: BLE001
        _manejar_error_supabase(error)

    if not respuesta.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un imprevisto con id={imprevisto_id}.",
        )

    return respuesta.data[0]


@router.delete(
    "/{imprevisto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un imprevisto registrado por error",
)
def eliminar_imprevisto(imprevisto_id: UUID) -> None:
    try:
        cliente = obtener_cliente()
        respuesta = (
            cliente.table(TABLA).delete().eq("id", str(imprevisto_id)).execute()
        )
    except (ConfiguracionSupabaseError, APIError) as error:
        _manejar_error_supabase(error)
    except Exception as error:  # noqa: BLE001
        _manejar_error_supabase(error)

    if not respuesta.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un imprevisto con id={imprevisto_id}.",
        )
