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

    def editar_usuario():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona", "Seleccione un usuario para editar")
            return

        valores = tree.item(seleccion[0], "values")
        user_id, nombre_actual, rol_actual = valores

        def guardar_edicion():
            nuevo_nombre = entry_nombre.get().strip()
            nueva_contra = entry_contrasena.get().strip()
            nuevo_rol = combo_rol.get()

            if not nuevo_nombre or not nueva_contra or not nuevo_rol:
                messagebox.showwarning("Advertencia", "Complete todos los campos")
                return

            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("UPDATE usuarios SET nombre=%s, contraseña=%s, rol=%s WHERE id=%s",
                               (nuevo_nombre, nueva_contra, nuevo_rol, user_id))
                conexion.commit()
                conexion.close()
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                ventana_editar.destroy()
                cargar_usuarios()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar usuario\n{e}")

        ventana_editar = tk.Toplevel()
        ventana_editar.title("Editar Usuario")
        ventana_editar.geometry("300x200")

        tk.Label(ventana_editar, text="Nuevo Nombre:").pack()
        entry_nombre = tk.Entry(ventana_editar)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack()

        tk.Label(ventana_editar, text="Nueva Contraseña:").pack()
        entry_contrasena = tk.Entry(ventana_editar, show="*")
        entry_contrasena.pack()

        tk.Label(ventana_editar, text="Nuevo Rol:").pack()
        combo_rol = ttk.Combobox(ventana_editar, values=["admin", "vendedor"], state="readonly")
        combo_rol.pack()
        combo_rol.set(rol_actual)

        tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_edicion).pack(pady=10)

    def eliminar_usuario():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona", "Seleccione un usuario para eliminar")
            return

        valores = tree.item(seleccion[0], "values")
        user_id, nombre, _ = valores

        confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar al usuario '{nombre}'?")
        if not confirmar:
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
            cargar_usuarios()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar usuario\n{e}")

    # Botones
    frame_botones = tk.Frame(parent)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Cargar Usuarios", command=cargar_usuarios).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Crear Usuario", command=crear_usuario).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Editar Usuario", command=editar_usuario).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Eliminar Usuario", command=eliminar_usuario).grid(row=0, column=3, padx=5)

    cargar_usuarios()
