import pandas as pd
from IPython.display import display, HTML

def obtener_datos_bitacora(supabase_client):
    """Consulta la tabla bitacora y retorna un DataFrame."""
    try:
        respuesta = supabase_client.table("bitacora").select("*").order("fecha", desc=True).execute()
        return pd.DataFrame(respuesta.data)
    except Exception as e:
        print("❌ Error al consultar Supabase:", e)
        return pd.DataFrame()

def renderizar_historial_html(df):
    """Genera la interfaz visual responsiva con colores."""
    if df is None or df.empty:
        print("⚠️ No hay registros guardados en la bitácora todavía.")
        return

    html_code = """
    <style>
        .contenedor-bitacora { font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: 0 auto; }
        .card-avance { border-radius: 8px; padding: 16px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); }
        .sin-imprevisto { background-color: #f0fdf4; border-left: 6px solid #16a34a; }
        .con-imprevisto { background-color: #fef2f2; border-left: 6px solid #dc2626; }
        .header-card { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .fecha { font-weight: bold; color: #334155; }
        .badge { padding: 4px 10px; border-radius: 12px; font-size: 0.85em; font-weight: bold; }
        .badge-success { background-color: #dcfce7; color: #15803d; }
        .badge-danger { background-color: #fee2e2; color: #b91c1c; }
        .texto-imprevisto { color: #991b1b; background-color: #fff1f1; padding: 8px 12px; border-radius: 6px; font-size: 0.9em; margin-top: 8px; border: 1px solid #fecaca; }
    </style>
    <div class="contenedor-bitacora">
        <h2 style="color: #0f172a; text-align: center; margin-bottom: 20px;">📋 Historial de Bitácora de Obra</h2>
    """

    for _, fila in df.iterrows():
        imprevisto_txt = str(fila.get('imprevisto', '')).strip()
        tiene_imprevisto = bool(imprevisto_txt and imprevisto_txt.lower() not in ['none', 'nan', 'null', ''])

        clase_card = "con-imprevisto" if tiene_imprevisto else "sin-imprevisto"
        badge_html = '<span class="badge badge-danger">🚨 Con Imprevisto</span>' if tiene_imprevisto else '<span class="badge badge-success">✅ Día Normal</span>'

        html_code += f"""
        <div class="card-avance {clase_card}">
            <div class="header-card">
                <span class="fecha">📅 Fecha: {fila.get('fecha', 'N/A')}</span>
                {badge_html}
            </div>
            <div><strong>Avance del día:</strong> {fila.get('descripcion_avance', 'Sin información')}</div>
        """

        if tiene_imprevisto:
            html_code += f"""
            <div class="texto-imprevisto">
                <strong>⚠️ Detalle del Imprevisto:</strong> {imprevisto_txt}
            </div>
            """

        html_code += "</div>"

    html_code += "</div>"
    display(HTML(html_code))
