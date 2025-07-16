from tkinter import simpledialog
import tkinter as tk
from tkinter import ttk
from app.db import conectar
from datetime import datetime

def cargar_vista(parent):
    carrito = []
    total_venta = tk.DoubleVar(master=parent, value=0.00)

    # --- FRAME PRINCIPAL ---
    main_frame = tk.Frame(parent)
    main_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # --- Mensaje temporal ---
    mensaje_label = tk.Label(main_frame, fg="red", font=("Arial", 10))
    mensaje_label.pack(anchor="w")

    def mostrar_mensaje(texto, color="green"):
        mensaje_label.config(text=texto, fg=color)
        mensaje_label.after(3000, lambda: mensaje_label.config(text=""))

    # --- Barra de búsqueda ---
    frame_busqueda = tk.Frame(main_frame)
    frame_busqueda.pack(anchor="w", pady=5)

    tk.Label(frame_busqueda, text="Buscar producto:").pack(side="left")
    entrada_busqueda = tk.Entry(frame_busqueda)
    entrada_busqueda.pack(side="left", padx=5)

    def buscar_productos():
        termino = entrada_busqueda.get().lower()
        for fila in tree_productos.get_children():
            tree_productos.delete(fila)
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, nombre, precio, stock FROM productos WHERE stock > 0 AND LOWER(nombre) LIKE %s",
                (f"%{termino}%",)
            )
            for producto in cursor.fetchall():
                tree_productos.insert("", "end", values=producto)
            conexion.close()
        except Exception as e:
            mostrar_mensaje(f"Error al buscar productos\n{e}", "red")

    tk.Button(frame_busqueda, text="Buscar", command=buscar_productos).pack(side="left", padx=5)

    # --- Tabla de productos ---
    tree_productos = ttk.Treeview(main_frame, columns=("ID", "Nombre", "Precio", "Stock"), show="headings", height=6)
    for col in ("ID", "Nombre", "Precio", "Stock"):
        tree_productos.heading(col, text=col)
        tree_productos.column(col, width=150)
    tree_productos.pack(pady=5, fill="x")

    def cargar_productos():
        for fila in tree_productos.get_children():
            tree_productos.delete(fila)
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, precio, stock FROM productos WHERE stock > 0")
            for producto in cursor.fetchall():
                tree_productos.insert("", "end", values=producto)
            conexion.close()
        except Exception as e:
            mostrar_mensaje(f"Error al cargar productos\n{e}", "red")

    # --- Tabla del carrito ---
    tree_carrito = ttk.Treeview(main_frame, columns=("ID", "Nombre", "Cantidad", "Subtotal"), show="headings", height=6)
    for col in ("ID", "Nombre", "Cantidad", "Subtotal"):
        tree_carrito.heading(col, text=col)
        tree_carrito.column(col, width=150)
    tree_carrito.pack(pady=5, fill="x")

    def agregar_al_carrito():
        selected = tree_productos.selection()
        if not selected:
            mostrar_mensaje("Seleccione un producto", "red")
            return

        item = tree_productos.item(selected[0])
        id_producto, nombre, precio, stock = item["values"]

        for prod in carrito:
            if prod["id"] == id_producto:
                mostrar_mensaje("Producto ya está en el carrito", "orange")
                return

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            mostrar_mensaje("Error en datos del producto", "red")
            return

        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese cantidad para '{nombre}' (Disponible: {stock}):", minvalue=1, maxvalue=stock)
        if cantidad is None:
            return

        if cantidad > stock:
            mostrar_mensaje("Cantidad supera el stock disponible", "red")
            return

        subtotal = round(precio * cantidad, 2)
        carrito.append({"id": id_producto, "nombre": nombre, "cantidad": cantidad, "subtotal": subtotal})
        tree_carrito.insert("", "end", values=(id_producto, nombre, cantidad, subtotal))

        total_actual = total_venta.get() + subtotal
        total_venta.set(round(total_actual, 2))
        lbl_total.config(text=f"Total: S/. {total_venta.get():.2f}")

    def registrar_venta():
        if not carrito:
            mostrar_mensaje("El carrito está vacío", "red")
            return
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute("INSERT INTO ventas (fecha, total) VALUES (%s, %s)", (datetime.now(), total_venta.get()))
            id_venta = cursor.lastrowid

            for item in carrito:
                cursor.execute("""
                    INSERT INTO detalle_venta (id_venta, id_producto, cantidad, subtotal) 
                    VALUES (%s, %s, %s, %s)
                """, (id_venta, item["id"], item["cantidad"], item["subtotal"]))

                cursor.execute("""
                    UPDATE productos SET stock = stock - %s WHERE id = %s
                """, (item["cantidad"], item["id"]))

            conexion.commit()
            conexion.close()

            mostrar_mensaje("Venta registrada correctamente", "green")
            carrito.clear()
            tree_carrito.delete(*tree_carrito.get_children())
            total_venta.set(0.00)
            lbl_total.config(text="Total: S/. 0.00")
            cargar_productos()

        except Exception as e:
            mostrar_mensaje(f"Error al registrar venta\n{e}", "red")

    # --- Botones ---
    frame_botones = tk.Frame(main_frame)
    frame_botones.pack(pady=5)

    tk.Button(frame_botones, text="Agregar al Carrito", command=agregar_al_carrito).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Registrar Venta", command=registrar_venta).grid(row=0, column=1, padx=5)

    lbl_total = tk.Label(main_frame, text="Total: S/. 0.00", font=("Arial", 16, "bold"))
    lbl_total.pack(pady=10)

    cargar_productos()