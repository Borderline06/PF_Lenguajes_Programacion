import tkinter as tk
from tkinter import ttk
from app.db import conectar
from app.utils import mostrar_mensaje_temporal

def cargar_vista(parent):
    tree = ttk.Treeview(parent, columns=("ID", "Nombre", "Categoría", "Precio", "Stock"), show="headings")
    for col in ("ID", "Nombre", "Categoría", "Precio", "Stock"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Cargar productos
    def cargar_productos():
        for fila in tree.get_children():
            tree.delete(fila)
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos")
            for producto in cursor.fetchall():
                tree.insert("", "end", values=producto)
            conexion.close()
        except Exception as e:
            mostrar_mensaje_temporal(parent, f"Error cargando productos: {e}", "red")

    # Agregar producto
    def agregar_producto():
        def guardar():
            nombre = entry_nombre.get().strip()
            categoria = entry_categoria.get().strip()
            precio = entry_precio.get().strip()
            stock = entry_stock.get().strip()

            if not nombre or not precio or not stock:
                mostrar_mensaje_temporal(ventana_agregar, "Complete los campos obligatorios", "orange")
                return

            try:
                precio = float(precio)
                stock = int(stock)
                if precio < 0 or stock < 0:
                    raise ValueError
            except ValueError:
                mostrar_mensaje_temporal(ventana_agregar, "Precio/stock inválido", "red")
                return

            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("SELECT COUNT(*) FROM productos WHERE nombre = %s", (nombre,))
                if cursor.fetchone()[0] > 0:
                    conexion.close()
                    mostrar_mensaje_temporal(ventana_agregar, "Ya existe un producto con ese nombre", "red")
                    return

                cursor.execute(
                    "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
                    (nombre, categoria, precio, stock)
                )
                conexion.commit()
                conexion.close()
                mostrar_mensaje_temporal(parent, "Producto agregado correctamente", "green")
                ventana_agregar.destroy()
                cargar_productos()
            except Exception as e:
                mostrar_mensaje_temporal(ventana_agregar, f"Error al guardar: {e}", "red")

        ventana_agregar = tk.Toplevel()
        ventana_agregar.title("Agregar Producto")
        ventana_agregar.geometry("300x250")

        tk.Label(ventana_agregar, text="Nombre:").pack()
        entry_nombre = tk.Entry(ventana_agregar)
        entry_nombre.pack()

        tk.Label(ventana_agregar, text="Categoría:").pack()
        entry_categoria = tk.Entry(ventana_agregar)
        entry_categoria.pack()

        tk.Label(ventana_agregar, text="Precio:").pack()
        entry_precio = tk.Entry(ventana_agregar)
        entry_precio.pack()

        tk.Label(ventana_agregar, text="Stock:").pack()
        entry_stock = tk.Entry(ventana_agregar)
        entry_stock.pack()

        tk.Button(ventana_agregar, text="Guardar", command=guardar).pack(pady=10)

    # Editar producto
    def editar_producto():
        selected = tree.selection()
        if not selected:
            mostrar_mensaje_temporal(parent, "Seleccione un producto", "orange")
            return

        item = tree.item(selected[0])
        id_producto, nombre_actual, categoria_actual, precio_actual, stock_actual = item["values"]

        def guardar_edicion():
            nuevo_nombre = entry_nombre.get().strip()
            nueva_categoria = entry_categoria.get().strip()
            nuevo_precio = entry_precio.get().strip()
            nuevo_stock = entry_stock.get().strip()

            if not nuevo_nombre or not nuevo_precio or not nuevo_stock:
                mostrar_mensaje_temporal(ventana_editar, "Complete todos los campos", "orange")
                return

            try:
                nuevo_precio = float(nuevo_precio)
                nuevo_stock = int(nuevo_stock)
                if nuevo_precio < 0 or nuevo_stock < 0:
                    raise ValueError
            except ValueError:
                mostrar_mensaje_temporal(ventana_editar, "Valores inválidos", "red")
                return

            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("""
                    UPDATE productos 
                    SET nombre = %s, categoria = %s, precio = %s, stock = %s 
                    WHERE id = %s
                """, (nuevo_nombre, nueva_categoria, nuevo_precio, nuevo_stock, id_producto))
                conexion.commit()
                conexion.close()
                mostrar_mensaje_temporal(parent, "Producto actualizado correctamente", "green")
                ventana_editar.destroy()
                cargar_productos()
            except Exception as e:
                mostrar_mensaje_temporal(ventana_editar, f"Error: {e}", "red")

        ventana_editar = tk.Toplevel()
        ventana_editar.title("Editar Producto")
        ventana_editar.geometry("300x250")

        tk.Label(ventana_editar, text="Nombre:").pack()
        entry_nombre = tk.Entry(ventana_editar)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack()

        tk.Label(ventana_editar, text="Categoría:").pack()
        entry_categoria = tk.Entry(ventana_editar)
        entry_categoria.insert(0, categoria_actual)
        entry_categoria.pack()

        tk.Label(ventana_editar, text="Precio:").pack()
        entry_precio = tk.Entry(ventana_editar)
        entry_precio.insert(0, precio_actual)
        entry_precio.pack()

        tk.Label(ventana_editar, text="Stock:").pack()
        entry_stock = tk.Entry(ventana_editar)
        entry_stock.insert(0, stock_actual)
        entry_stock.pack()

        tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_edicion).pack(pady=10)

    # Eliminar producto
    def eliminar_producto():
        selected = tree.selection()
        if not selected:
            mostrar_mensaje_temporal(parent, "Seleccione un producto para eliminar", "orange")
            return

        item = tree.item(selected[0])
        id_producto = item["values"][0]

        confirm = tk.messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este producto?")
        if confirm:
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
                conexion.commit()
                conexion.close()
                mostrar_mensaje_temporal(parent, "Producto eliminado", "green")
                cargar_productos()
            except Exception as e:
                mostrar_mensaje_temporal(parent, f"Error eliminando: {e}", "red")

    # Botones
    frame_botones = tk.Frame(parent)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Cargar Productos", command=cargar_productos).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Agregar", command=agregar_producto).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Editar", command=editar_producto).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Eliminar", command=eliminar_producto).grid(row=0, column=3, padx=5)

    cargar_productos()