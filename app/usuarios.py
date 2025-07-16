import tkinter as tk
from tkinter import ttk, messagebox
from app.db import conectar

def cargar_vista(parent):
    tree = ttk.Treeview(parent, columns=("ID", "Nombre", "Rol"), show="headings")
    for col in ("ID", "Nombre", "Rol"):
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="x", pady=10, padx=10)

    def cargar_usuarios():
        for fila in tree.get_children():
            tree.delete(fila)
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, rol FROM usuarios")
            for usuario in cursor.fetchall():
                tree.insert("", "end", values=usuario)
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar usuarios\n{e}")

    def crear_usuario():
        def guardar():
            nombre = entry_nombre.get().strip()
            contrasena = entry_contrasena.get().strip()
            rol = combo_rol.get()

            if not nombre or not contrasena or not rol:
                messagebox.showwarning("Advertencia", "Complete todos los campos")
                return

            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nombre = %s", (nombre,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showwarning("Duplicado", "Ya existe un usuario con ese nombre")
                    return

                cursor.execute("INSERT INTO usuarios (nombre, contraseña, rol) VALUES (%s, %s, %s)",
                               (nombre, contrasena, rol))
                conexion.commit()
                conexion.close()
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
                ventana_crear.destroy()
                cargar_usuarios()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear usuario\n{e}")

        ventana_crear = tk.Toplevel()
        ventana_crear.title("Crear Usuario")
        ventana_crear.geometry("300x200")

        tk.Label(ventana_crear, text="Nombre:").pack()
        entry_nombre = tk.Entry(ventana_crear)
        entry_nombre.pack()

        tk.Label(ventana_crear, text="Contraseña:").pack()
        entry_contrasena = tk.Entry(ventana_crear, show="*")
        entry_contrasena.pack()

        tk.Label(ventana_crear, text="Rol:").pack()
        combo_rol = ttk.Combobox(ventana_crear, values=["admin", "vendedor"], state="readonly")
        combo_rol.pack()
        combo_rol.set("vendedor")

        tk.Button(ventana_crear, text="Guardar", command=guardar).pack(pady=10)

    # Botones
    frame_botones = tk.Frame(parent)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Cargar Usuarios", command=cargar_usuarios).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Crear Usuario", command=crear_usuario).grid(row=0, column=1, padx=5)

    cargar_usuarios()