import tkinter as tk
from tkinter import messagebox
from tabla import RecordTable
from ull import API
from tkinter import ttk




class RecordViewer(tk.Tk):
    def __init__(self, api):
        super().__init__()
        self.__api = api
        self.__init_ui()

    def __init_ui(self):
        self.title("UNSC")
        self.geometry("1200x800")
        self.resizable(False, False)

        self.__table = RecordTable(self)
        self.__load_records()

        self.__actualizacion_tabla = tk.Button(self, text="Actualizar Tabla", command=self.nuevos_registros)
        self.__actualizacion_tabla.pack(pady=10)


        self.__input_button = tk.Button(self, text="Buscar Registro por Generación", command=self.__input_record_id)
        self.__input_button.pack(pady=10)

    def registros_iniciales(self):
        records = self.__api.fetch_records()
        self.__table.load_records(records)

    def nuevos_registros(self):
        self.__load_records()
        self.__table.load_records()
        messagebox.showinfo("Actualización", "La tabla ha sido actualizada exitosamente.")

    def __load_records(self):
        records = self.__api.fetch_records()
        self.__table.load_records(records)



    def __input_record_id(self):
        input_window = tk.Toplevel(self)
        input_window.title("Buscar Generación")
        input_window.geometry("300x150")

        tk.Label(input_window, text="Ingresa la generación:").pack(pady=10)
        entry = tk.Entry(input_window)
        entry.pack(pady=5)

        tk.Button(input_window, text="Buscar", command=lambda: self.__search_record(entry.get(), input_window)).pack(pady=10)

    def __search_record(self, record_id, input_window):
        try:
            record = self.__api.fetch_record_by_id(record_id)
            if record:
                self.__show_record_details(record)
            else:
                messagebox.showwarning("Advertencia", "Registro no encontrado.")
        except ValueError:
            messagebox.showwarning("Advertencia", "Por favor, ingrese la generación.")
        input_window.destroy()

    def __show_record_details(self, record):
        detail_window = tk.Toplevel(self)
        detail_window.title("Detalles del Registro de Usuario")
        detail_window.geometry("1200x500")
        detail_window.resizable(False, False)
        detail_table = RecordTable(detail_window)
        detail_table.pack(expand=True, fill='both')
        detail_table.load_records([record])


