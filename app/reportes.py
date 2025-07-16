import tkinter as tk
from tkinter import ttk, messagebox
from app.db import conectar

def cargar_vista(parent):
    # Tabla de ventas
    tree_ventas = ttk.Treeview(parent, columns=("ID", "Fecha", "Total"), show="headings")
    for col in ("ID", "Fecha", "Total"):
        tree_ventas.heading(col, text=col)
        tree_ventas.column(col, width=200)
    tree_ventas.pack(pady=10, fill="x", padx=10)

    # Función para cargar las ventas
    def cargar_ventas():
        for fila in tree_ventas.get_children():
            tree_ventas.delete(fila)
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, fecha, total FROM ventas ORDER BY fecha DESC")
            for venta in cursor.fetchall():
                tree_ventas.insert("", "end", values=venta)
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las ventas\n{e}")

    # Función para ver detalle de una venta
    def ver_detalle():
        selected = tree_ventas.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una venta")
            return
        item = tree_ventas.item(selected[0])
        id_venta = item["values"][0]

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT p.nombre, d.cantidad, d.subtotal
                FROM detalle_venta d
                JOIN productos p ON d.id_producto = p.id
                WHERE d.id_venta = %s
            """, (id_venta,))
            detalles = cursor.fetchall()
            conexion.close()

            detalle_texto = "\n".join([
                f"{nombre} - Cantidad: {cantidad} - Subtotal: S/. {subtotal:.2f}"
                for nombre, cantidad, subtotal in detalles
            ])

            messagebox.showinfo("Detalle de Venta", detalle_texto or "No hay detalles")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener detalle\n{e}")

    # Botones
    frame_botones = tk.Frame(parent)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Cargar Ventas", command=cargar_ventas).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Ver Detalle", command=ver_detalle).grid(row=0, column=1, padx=5)

    cargar_ventas()