import tkinter as tk
from tkinter import ttk
from app import productos, ventas, reportes, usuarios

def mostrar_interfaz(usuario, rol): 
    root = tk.Tk()
    root.title(f"MiniMarket Pro - {usuario} ({rol})")
    root.geometry("900x600")
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    if rol == "admin":
        frame_productos = ttk.Frame(notebook)
        notebook.add(frame_productos, text="Productos")
        productos.cargar_vista(frame_productos)

        frame_usuarios = ttk.Frame(notebook)
        notebook.add(frame_usuarios, text="Usuarios")
        usuarios.cargar_vista(frame_usuarios)

    frame_ventas = ttk.Frame(notebook)
    notebook.add(frame_ventas, text="Ventas")
    ventas.cargar_vista(frame_ventas)

    frame_reportes = ttk.Frame(notebook)
    notebook.add(frame_reportes, text="Reportes")
    reportes.cargar_vista(frame_reportes)

    def al_cambiar_pestaña(event):
        pestaña_actual = event.widget.tab(event.widget.index("current"))["text"]
        if pestaña_actual == "Ventas" and hasattr(ventas, "actualizar_productos_en_tabla"):
            ventas.actualizar_productos_en_tabla()

    notebook.bind("<<NotebookTabChanged>>", al_cambiar_pestaña)

    # Botón de salir (centrado y con diseño limpio)
    frame_salida = tk.Frame(root)
    frame_salida.pack(pady=10)

    btn_salir = tk.Button(
        frame_salida, text="Cerrar Sesión",
        bg="#d9534f", fg="white",
        font=("Arial", 10, "bold"),
        command=root.destroy
    )
    btn_salir.pack()

    root.mainloop()