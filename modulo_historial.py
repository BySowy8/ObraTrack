import pandas as pd
from IPython.display import display, HTML
from supabase import create_client

def obtener_datos_bitacora(supabase_client):
    """
    Obtiene todos los registros de la tabla 'bitacora' desde Supabase.
    """
    try:
        response = supabase_client.table("bitacora").select("*").execute()
        data = response.data
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return pd.DataFrame()

def renderizar_historial_html(df):
    """
    Renderiza el historial con un diseño minimalista, limpio y tipo software real.
    """
    if df.empty:
        display(HTML("""
            <div style="font-family: monospace; padding: 15px; border: 1px solid #ddd; background: #fafafa; color: #555; max-width: 600px;">
                [Aviso] No hay registros en la bitácora todavía.
            </div>
        """))
        return

    # Estilo minimalista, plano, sin sombras de IA y tipografía neutra
    estilos = """
    <style>
        .obratrack-container {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 20px 0;
            max-width: 900px;
        }
        .obratrack-title {
            font-size: 16px;
            font-weight: 600;
            color: #222;
            margin-bottom: 8px;
            border-bottom: 1px solid #eaeaea;
            padding-bottom: 6px;
        }
        .obratrack-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            color: #333;
            background: #ffffff;
            border: 1px solid #e1e4e8;
        }
        .obratrack-table th {
            background-color: #f6f8fa;
            color: #24292e;
            font-weight: 600;
            text-align: left;
            padding: 8px 12px;
            border-bottom: 1px solid #e1e4e8;
        }
        .obratrack-table td {
            padding: 8px 12px;
            border-bottom: 1px solid #eaeaea;
        }
        .obratrack-table tr:hover {
            background-color: #f8f9fa;
        }
    </style>
    """

    # Convertimos el DataFrame a HTML limpio
    tabla_html = df.to_html(classes='obratrack-table', index=False, border=0)
    
    html_final = f"""
    {estilos}
    <div class="obratrack-container">
        <div class="obratrack-title">Historial de ObraTrack (Bitácora)</div>
        {tabla_html}
    </div>
    """
    
    display(HTML(html_final))
