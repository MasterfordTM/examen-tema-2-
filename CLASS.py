import tkinter as tk
from tkinter import messagebox
from tabla import RecordTable
from ull import API



class RecordViewer(tk.Tk):
    def __init__(self, api):
        super().__init__()
        self.__api = api
        self.__init_ui()

    def __init_ui(self):
        self.title("UNSC")
        self.geometry("1000x500")
        self.resizable(False, False)

        self.__table = RecordTable(self)
        self.__load_records()

        self.__input_button = tk.Button(self, text="Buscar Registro por Generación", command=self.__input_record_id)
        self.__input_button.pack(pady=10)

    def __load_records(self):
        records = self.__api.fetch_records()
        self.__table.load_records(records)

        random_record = self.__api.fetch_random_record()
        if random_record:
            messagebox.showinfo(
                "Registro Aleatorio",
                f"Registro Aleatorio:\nGeneración: {random_record.get('generacion', 'N/A')}\n"
                f"Spartan: {random_record.get('spartan', 'N/A')}\nApellido: {random_record.get('apellido', 'N/A')}\n"
                f"Ciudad: {random_record.get('ciudad', 'N/A')}\nPlantel de Entrenamiento: {random_record.get('planteldeentrenamiento', 'N/A')}\n"
                f"Estado: {random_record.get('estadodemision', 'N/A')}"
            )

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
        detail_window.geometry("600x400")

        tk.Label(detail_window, text="Generación: " + str(record.get('generacion', 'N/A'))).pack(pady=20)
        tk.Label(detail_window, text="Spartan: " + record.get('spartan', 'N/A')).pack(pady=10)
        tk.Label(detail_window, text="Apellido: " + record.get('apellido', 'N/A')).pack(pady=10)
        tk.Label(detail_window, text="Ciudad: " + record.get('ciudad', 'N/A')).pack(pady=10)
        tk.Label(detail_window, text="Estado: " + record.get('estadodemision', 'N/A')).pack(pady=10)
        tk.Label(detail_window, text="Plantel de Entrenamiento: " + record.get('planteldeentrenamiento', 'N/A')).pack(pady=10)