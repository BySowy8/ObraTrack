"""
Punto único de conexión a Supabase.

Nunca pongas la URL ni la API key directamente en el código (y mucho menos
las subas a GitHub). Se leen desde variables de entorno. En Colab las vas
a definir con `os.environ`, y en tu máquina/servidor con un archivo `.env`.
"""

import os

from supabase import Client, create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

_client: Client | None = None


class ConfiguracionSupabaseError(RuntimeError):
    """Se lanza cuando faltan las credenciales de Supabase."""


def obtener_cliente() -> Client:
    """
    Devuelve un cliente de Supabase ya configurado (patrón singleton simple).

    Lanza ConfiguracionSupabaseError si las variables de entorno no están
    definidas, en vez de fallar con un error críptico de conexión más
    adelante. Esto es parte del requisito de "Manejo de Errores Visible".
    """
    global _client

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ConfiguracionSupabaseError(
            "Faltan las variables de entorno SUPABASE_URL y/o SUPABASE_KEY. "
            "Defínelas antes de iniciar la aplicación."
        )

    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)

    return _client
