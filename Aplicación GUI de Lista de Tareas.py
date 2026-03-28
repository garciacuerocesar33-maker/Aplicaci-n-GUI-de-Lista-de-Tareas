import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


class TodoApp:
    def __init__(self, root):
        """
        Inicializa la aplicación de lista de tareas.
        Configura la ventana principal y todos los componentes de la interfaz.
        """
        self.root = root
        self.root.title("Lista de Tareas - Todo App")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Lista para almacenar las tareas: cada tarea es un diccionario con 'texto' y 'completada'
        self.tareas = []
        self.tarea_seleccionada = None

        # Cargar tareas guardadas si existen
        self.cargar_tareas()

        self.setup_ui()
        self.actualizar_lista_tareas()

    def setup_ui(self):
        """
        Configura todos los elementos de la interfaz gráfica.
        Incluye frame principal, entrada de texto, botones y lista de tareas.
        """
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar peso de las filas y columnas para redimensionamiento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Título de la aplicación
        titulo = ttk.Label(main_frame, text="📝 Lista de Tareas",
                           font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Frame para entrada de nueva tarea
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)

        # Campo de entrada para nueva tarea
        self.entry_tarea = ttk.Entry(input_frame, font=("Arial", 11))
        self.entry_tarea.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.entry_tarea.bind('<Return>', lambda event: self.anadir_tarea())  # Enter para añadir
        self.entry_tarea.focus()  # Foco automático en el campo

        # Botón Añadir Tarea
        self.btn_anadir = ttk.Button(input_frame, text="➕ Añadir Tarea",
                                     command=self.anadir_tarea)
        self.btn_anadir.grid(row=0, column=1)

        # Frame para botones de acción
        botones_frame = ttk.Frame(main_frame)
        botones_frame.grid(row=2, column=0, columnspan=3, pady=(0, 10))

        # Botón Marcar como Completada
        self.btn_completar = ttk.Button(botones_frame, text="✅ Marcar Completada",
                                        command=self.marcar_completada,
                                        state='disabled')
        self.btn_completar.grid(row=0, column=0, padx=(0, 10))

        # Botón Eliminar
        self.btn_eliminar = ttk.Button(botones_frame, text="🗑️ Eliminar Tarea",
                                       command=self.eliminar_tarea,
                                       state='disabled')
        self.btn_eliminar.grid(row=0, column=1, padx=(0, 10))

        # Botón Limpiar Completadas
        self.btn_limpiar = ttk.Button(botones_frame, text="🧹 Limpiar Completadas",
                                      command=self.limpiar_completadas)
        self.btn_limpiar.grid(row=0, column=2)

        # Lista de tareas con scrollbar
        lista_frame = ttk.Frame(main_frame)
        lista_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        lista_frame.columnconfigure(0, weight=1)
        lista_frame.rowconfigure(0, weight=1)

        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(lista_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Listbox para mostrar las tareas
        self.lista_tareas = tk.Listbox(lista_frame, font=("Arial", 10),
                                       selectmode=tk.SINGLE,
                                       yscrollcommand=scrollbar.set,
                                       height=15)
        self.lista_tareas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.lista_tareas.yview)

        # Evento de selección en la lista
        self.lista_tareas.bind('<<ListboxSelect>>', self.on_tarea_seleccionada)
        # Doble clic para marcar como completada
        self.lista_tareas.bind('<Double-Button-1>', lambda event: self.marcar_completada())

    def anadir_tarea(self):
        """
        Añade una nueva tarea a la lista.
        Se activa con el botón o presionando Enter.
        """
        texto = self.entry_tarea.get().strip()
        if texto:
            # Crear nueva tarea sin completar
            nueva_tarea = {'texto': texto, 'completada': False}
            self.tareas.append(nueva_tarea)

            # Limpiar entrada y actualizar lista
            self.entry_tarea.delete(0, tk.END)
            self.actualizar_lista_tareas()
            self.guardar_tareas()

            # Mensaje de confirmación
            messagebox.showinfo("Éxito", f"✅ Tarea '{texto}' añadida correctamente!")
        else:
            messagebox.showwarning("Advertencia", "⚠️ Por favor, escribe una tarea.")

    def marcar_completada(self):
        """
        Marca la tarea seleccionada como completada o desmarca si ya está completada.
        Se activa con botón o doble clic.
        """
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            indice = seleccion[0]
            self.tareas[indice]['completada'] = not self.tareas[indice]['completada']
            self.actualizar_lista_tareas()
            self.guardar_tareas()

    def eliminar_tarea(self):
        """
        Elimina la tarea seleccionada de la lista.
        """
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            indice = seleccion[0]
            tarea_texto = self.tareas[indice]['texto']
            confirmacion = messagebox.askyesno("Confirmar Eliminación",
                                               f"¿Estás seguro de eliminar la tarea:\n'{tarea_texto}'?")
            if confirmacion:
                self.tareas.pop(indice)
                self.actualizar_lista_tareas()
                self.guardar_tareas()
                messagebox.showinfo("Eliminada", "✅ Tarea eliminada correctamente.")

    def limpiar_completadas(self):
        """
        Elimina todas las tareas marcadas como completadas.
        """
        completadas = [tarea for tarea in self.tareas if tarea['completada']]
        if completadas:
            confirmacion = messagebox.askyesno("Limpiar Completadas",
                                               f"¿Eliminar {len(completadas)} tarea(s) completada(s)?")
            if confirmacion:
                self.tareas = [tarea for tarea in self.tareas if not tarea['completada']]
                self.actualizar_lista_tareas()
                self.guardar_tareas()
        else:
            messagebox.showinfo("Info", "ℹ️ No hay tareas completadas para eliminar.")

    def on_tarea_seleccionada(self, event):
        """
        Maneja la selección de una tarea en la lista.
        Habilita/deshabilita botones según el estado de la tarea.
        """
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            self.tarea_seleccionada = seleccion[0]
            # Habilitar botones de acción
            self.btn_completar.config(state='normal')
            self.btn_eliminar.config(state='normal')
        else:
            self.tarea_seleccionada = None
            self.btn_completar.config(state='disabled')
            self.btn_eliminar.config(state='disabled')

    def actualizar_lista_tareas(self):
        """
        Actualiza la visualización de la lista de tareas.
        Tareas completadas aparecen tachadas y en gris.
        """
        # Limpiar lista actual
        self.lista_tareas.delete(0, tk.END)

        for i, tarea in enumerate(self.tareas):
            texto = tarea['texto']
            if tarea['completada']:
                # Tarea completada: tachada y gris
                display_texto = f"✅ {texto}"
                self.lista_tareas.insert(tk.END, display_texto)
                # Configurar color para tarea completada
                self.lista_tareas.itemconfig(i, {'fg': '#888888'})
            else:
                # Tarea pendiente: normal
                display_texto = f"⭕ {texto}"
                self.lista_tareas.insert(tk.END, display_texto)

        # Actualizar título con contador
        pendientes = len([t for t in self.tareas if not t['completada']])
        completadas = len([t for t in self.tareas if t['completada']])
        self.root.title(f"Lista de Tareas - {pendientes} pendientes, {completadas} completadas")

    def guardar_tareas(self):
        """
        Guarda las tareas en un archivo JSON para persistencia.
        """
        try:
            with open('tareas.json', 'w', encoding='utf-8') as f:
                json.dump(self.tareas, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar tareas: {e}")

    def cargar_tareas(self):
        """
        Carga las tareas guardadas desde archivo JSON.
        """
        try:
            with open('tareas.json', 'r', encoding='utf-8') as f:
                self.tareas = json.load(f)
        except FileNotFoundError:
            self.tareas = []
        except Exception as e:
            print(f"Error al cargar tareas: {e}")
            self.tareas = []


def main():
    """
    Función principal para ejecutar la aplicación.
    """
    root = tk.Tk()
    app = TodoApp(root)

    # Manejar cierre de ventana
    def on_closing():
        app.guardar_tareas()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()