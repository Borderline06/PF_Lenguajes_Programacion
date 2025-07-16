import tkinter as tk
from tkinter import messagebox
from app import interfaz  
from app.db import conectar

def ventana_login():
    ventana = tk.Tk()
    ventana.title("MiniMarket Pro - Login")
    ventana.geometry("300x200")

    tk.Label(ventana, text="Usuario:").pack(pady=5)
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()

    tk.Label(ventana, text="Contraseña:").pack(pady=5)
    entry_contrasena = tk.Entry(ventana, show="*")
    entry_contrasena.pack()

    def iniciar_sesion():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        if not usuario or not contrasena:
            messagebox.showwarning("Advertencia", "Complete ambos campos")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, rol FROM usuarios WHERE nombre = %s AND contraseña = %s", (usuario, contrasena))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                nombre_usuario, rol = resultado
                messagebox.showinfo("Éxito", f"Bienvenido, {nombre_usuario} ({rol})")
                ventana.destroy()
                interfaz.mostrar_interfaz(usuario=nombre_usuario, rol=rol) 
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar sesión\n{e}")

    tk.Button(ventana, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)
    ventana.mainloop()