import tkinter as tk
from tkinter import messagebox

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Lista de Tareas")
ventana.geometry("500x500")

# Lista de tareas
tareas = []
check_vars = {}

# Función para agregar tarea
def agregar_tarea():
    tarea = entrada_tarea.get()
    if tarea != "":
        tareas.append(tarea)
        check_vars[tarea] = tk.BooleanVar()  # Crear una variable para el checkbox
        actualizar_lista()
        entrada_tarea.delete(0, tk.END)  # Limpiar entrada
    else:
        messagebox.showwarning("Advertencia", "Por favor ingrese una tarea.")

# Función para eliminar tarea
def eliminar_tarea(tarea):
    tareas.remove(tarea)
    del check_vars[tarea]  # Eliminar la variable del checkbox
    actualizar_lista()

# Función para actualizar lista de tareas
def actualizar_lista():
    # Limpiar la lista de tareas mostradas
    for widget in lista_tareas.winfo_children():
        widget.destroy()

    # Reordenar las tareas: las no completadas primero, luego las completadas
    tareas_ordenadas = [tarea for tarea in tareas if "(Completada)" not in tarea]
    tareas_completadas = [tarea for tarea in tareas if "(Completada)" in tarea]
    tareas_finales = tareas_ordenadas + tareas_completadas

    # Crear los widgets de las tareas
    for tarea in tareas_finales:
        frame_tarea = tk.Frame(lista_tareas)
        frame_tarea.pack(anchor="w", pady=2)

        # Crear checkbox para marcar como completada
        checkbutton = tk.Checkbutton(frame_tarea, text=tarea, variable=check_vars[tarea], command=actualizar_tareas_completadas)
        checkbutton.pack(side="left")

        # Botón de eliminar
        boton_eliminar = tk.Button(frame_tarea, text="-", command=lambda tarea=tarea: eliminar_tarea(tarea))
        boton_eliminar.pack(side="right")

# Función para actualizar las tareas completadas
def actualizar_tareas_completadas():
    global tareas
    tareas_actualizadas = []
    
    # Evitar cambios en el diccionario durante la iteración
    for tarea in list(check_vars.keys()):
        if check_vars[tarea].get():  # Si el checkbox está marcado
            if "(Completada)" not in tarea:
                tarea_completada = tarea + " (Completada)"
                check_vars[tarea_completada] = check_vars.pop(tarea)  # Mover la variable
                tareas_actualizadas.append(tarea_completada)
            else:
                tareas_actualizadas.append(tarea)
        else:
            tareas_actualizadas.append(tarea)
    
    tareas = tareas_actualizadas  # Actualizamos lista de tareas
    actualizar_lista()

# Widgets paraentrada de tarea y botones
entrada_tarea = tk.Entry(ventana, width=30)
entrada_tarea.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

boton_agregar = tk.Button(ventana, text="Nueva tarea (+)", command=agregar_tarea)
boton_agregar.grid(row=0, column=1, padx=10, pady=10)

# frame de las tareas
# Canvas para las tareas
canvas = tk.Canvas(ventana)
canvas.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

# Scrollbar vertical
scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
scrollbar.grid(row=1, column=2, sticky="ns", pady=10)

canvas.configure(yscrollcommand=scrollbar.set)

# Frame interno dentro del canvas
lista_tareas = tk.Frame(canvas)
canvas.create_window((0, 0), window=lista_tareas, anchor="nw")

# Ajustar el scroll automáticamente
def configurar_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

lista_tareas.bind("<Configure>", configurar_scroll)
def _on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Enlazar el evento del mousewheel al canvas
canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

# Permitir que el canvas se expanda
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_columnconfigure(0, weight=1)


# Ejecutar la aplicación
ventana.mainloop()
