import tkinter as tk

def mostrar_mensaje_temporal(widget_padre, mensaje, color="green", duracion=3000):
    for widget in widget_padre.pack_slaves():
        if getattr(widget, "_temporal", False):
            widget.destroy()

    etiqueta = tk.Label(widget_padre, text=mensaje, fg="white", bg=color, font=("Arial", 10, "bold"))
    etiqueta._temporal = True
    etiqueta.pack(side="bottom", fill="x", pady=(5, 0))
    widget_padre.after(duracion, etiqueta.destroy)