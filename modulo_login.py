import ipywidgets as widgets
from IPython.display import display, clear_output

class SistemaAuth:
    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.usuario_actual = None

    def autenticar(self, correo, contrasena):
        try:
            response = self.supabase.table("Usuarios").select("*").eq("correo", correo).eq("contrasena", contrasena).execute()
            datos = response.data
            if datos and len(datos) > 0:
                self.usuario_actual = datos[0]
                return True, f"¡Bienvenido! Has iniciado sesión como: {self.usuario_actual.get('rol', 'Usuario')}"
            else:
                return False, "Correo o contraseña incorrectos."
        except Exception as e:
            return False, f"Error de conexión: {e}"

    def registrar_usuario(self, correo, contrasena, rol):
        try:
            verificacion = self.supabase.table("Usuarios").select("*").eq("correo", correo).execute()
            if verificacion.data and len(verificacion.data) > 0:
                return False, "Ese correo ya está registrado en el sistema."

            nuevo_usuario = {
                "correo": correo,
                "contrasena": contrasena,
                "rol": rol
            }
            response = self.supabase.table("Usuarios").insert(nuevo_usuario).execute()
            
            if response.data:
                return True, "✅ Usuario creado exitosamente. Ve a la pestaña 'Login' para ingresar."
            return False, "No se pudo registrar el usuario."
        except Exception as e:
            return False, f"Error de conexión: {e}"

def mostrar_interfaz_auth(auth_sistema):
    titulo_login = widgets.HTML(value="<h3 style='color: #24292e;'>Iniciar Sesión</h3>")
    correo_login = widgets.Text(description="Correo:")
    pass_login = widgets.Password(description="Contraseña:")
    btn_login = widgets.Button(description="Ingresar", button_style='primary')
    salida_login = widgets.Output()

    def al_presionar_login(b):
        with salida_login:
            clear_output()
            correo = correo_login.value.strip()
            contrasena = pass_login.value.strip()

            if not correo or not contrasena:
                display(widgets.HTML("<div style='color: orange;'>⚠️ Llena todos los campos.</div>"))
                return

            btn_login.description = "Validando..."
            exito, mensaje = auth_sistema.autenticar(correo, contrasena)
            btn_login.description = "Ingresar"

            if exito:
                display(widgets.HTML(f"<div style='color: green; padding: 10px; background: #e6ffed; border: 1px solid #34d058; border-radius: 5px;'>✅ {mensaje}</div>"))
            else:
                display(widgets.HTML(f"<div style='color: red; padding: 10px; background: #ffeef0; border: 1px solid #d73a49; border-radius: 5px;'>❌ {mensaje}</div>"))

    btn_login.on_click(al_presionar_login)
    caja_login = widgets.VBox([titulo_login, correo_login, pass_login, btn_login, salida_login])

    titulo_reg = widgets.HTML(value="<h3 style='color: #24292e;'>Crear Nuevo Usuario</h3>")
    correo_reg = widgets.Text(description="Correo:")
    pass_reg = widgets.Password(description="Contraseña:")
    rol_reg = widgets.Dropdown(description="Rol:", options=['Contratista', 'Cliente'], value='Contratista')
    btn_reg = widgets.Button(description="Registrar", button_style='success')
    salida_reg = widgets.Output()

    def al_presionar_registro(b):
        with salida_reg:
            clear_output()
            correo = correo_reg.value.strip()
            contrasena = pass_reg.value.strip()
            rol = rol_reg.value

            if not correo or not contrasena:
                display(widgets.HTML("<div style='color: orange;'>⚠️ Llena todos los campos.</div>"))
                return

            btn_reg.description = "Guardando..."
            exito, mensaje = auth_sistema.registrar_usuario(correo, contrasena, rol)
            btn_reg.description = "Registrar"

            if exito:
                display(widgets.HTML(f"<div style='color: green;'>{mensaje}</div>"))
                correo_reg.value = ""
                pass_reg.value = ""
            else:
                display(widgets.HTML(f"<div style='color: red;'>❌ {mensaje}</div>"))

    btn_reg.on_click(al_presionar_registro)
    caja_registro = widgets.VBox([titulo_reg, correo_reg, pass_reg, rol_reg, btn_reg, salida_reg])

    pestanas = widgets.Tab(children=[caja_login, caja_registro])
    pestanas.set_title(0, 'Login')
    pestanas.set_title(1, 'Registro')
    
    display(pestanas)
