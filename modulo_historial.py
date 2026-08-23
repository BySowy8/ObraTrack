import pandas as pd
from IPython.display import display, HTML

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
    Renderiza el historial con diseño minimalista y diferencia visual para imprevistos.
    """
    if df.empty:
        display(HTML("""
            <div style="font-family: -apple-system, sans-serif; padding: 15px; border: 1px solid #e1e4e8; background: #f6f8fa; color: #586069; font-size: 13px; max-width: 900px;">
                [Aviso] No hay registros en la bitácora todavía.
            </div>
        """))
        return

    # Estilos CSS limpios y adaptados para imprevistos
    estilos = """
    <style>
        .obratrack-container {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 20px 0;
            max-width: 900px;
        }
        .obratrack-title {
            font-size: 15px;
            font-weight: 600;
            color: #24292e;
            margin-bottom: 8px;
            border-bottom: 1px solid #eaeaea;
            padding-bottom: 6px;
        }
        .obratrack-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            color: #24292e;
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
            vertical-align: top;
        }
        .obratrack-table tr:hover {
            background-color: #f8f9fa;
        }
        /* Estilo sutil para filas con imprevistos */
        .fila-imprevisto {
            background-color: #fffdfd;
        }
        .badge-imprevisto {
            display: inline-block;
            padding: 2px 6px;
            font-size: 11px;
            font-weight: 500;
            color: #d73a49;
            background-color: #ffeef0;
            border: 1px solid rgba(27,31,35,0.15);
            border-radius: 3px;
            margin-top: 4px;
        }
        .badge-normal {
            color: #28a745;
            font-size: 12px;
        }
    </style>
    """

    # Construimos las filas de la tabla manualmente para inyectar la lógica de imprevistos
    filas_html = ""
    for _, row in df.iterrows():
        fecha = row.get('fecha', 'Sin fecha')
        avance = row.get('descripcion_avance', 'Sin descripción')
        imprevisto = row.get('imprevisto', None)

        if imprevisto and str(imprevisto).strip() and str(imprevisto).lower() != 'none':
            # Si hay imprevisto
            estado_html = f"<span class='badge-imprevisto'> IMPREVISTO: {imprevisto}</span>"
            clase_fila = "fila-imprevisto"
        else:
            estado_html = "<span class='badge-normal'>✓ Normal</span>"
            clase_fila = ""

        filas_html += f"""
        <tr class="{clase_fila}">
            <td style="white-space: nowrap; width: 110px;">{fecha}</td>
            <td>{avance}</td>
            <td style="width: 250px;">{estado_html}</td>
        </tr>
        """

    html_final = f"""
    {estilos}
    <div class="obratrack-container">
        <div class="obratrack-title">Historial de Avances (Bitácora)</div>
        <table class="obratrack-table">
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Avance del Día</th>
                    <th>Estado / Observación</th>
                </tr>
            </thead>
            <tbody>
                {filas_html}
            </tbody>
        </table>
    </div>
    """
    
    display(HTML(html_final))
