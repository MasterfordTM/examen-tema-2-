import tkinter as tk
from tkinter import ttk, messagebox
import requests
import random

class API:
    def __init__(self, base_url):
        self.__base_url = base_url

    def fetch_records(self):
        try:
            response = requests.get(self.__base_url)
            response.raise_for_status()
            return response.json() if isinstance(response.json(), list) else []
        except (requests.RequestException, ValueError):
            return []

    def fetch_random_record(self):
        records = self.fetch_records()
        return random.choice(records) if records else None

    def fetch_record_by_id(self, record_id):
        records = self.fetch_records()
        for record in records:
            if str(record.get('generacion')) == str(record_id):
                return record
        return None

class RecordViewer(tk.Tk):
    def __init__(self, api):
        super().__init__()
        self.__api = api
        self.__init_ui()
        self.__load_records()

    def __init_ui(self):
        self.title("Registro de Usuarios")
        self.geometry("1000x500")
        self.resizable(False, False)

        # Ensure the column names match your data keys
        self.__tree = ttk.Treeview(self, columns=("generacion", "spartan", "apellido", "ciudad", "colonia"), show="headings")
        self.__tree.heading("generacion", text="Generación")
        self.__tree.heading("spartan", text="Spartan")
        self.__tree.heading("apellido", text="Apellido")
        self.__tree.heading("ciudad", text="Ciudad")
        self.__tree.heading("colonia", text="Colonia")
        self.__tree.pack(expand=True, fill='both')

        self.__input_button = tk.Button(self, text="Buscar Registro por Generación", command=self.__input_record_id)
        self.__input_button.pack(pady=10)

    def __load_records(self):
        # Clear existing records from the TreeView
        for item in self.__tree.get_children():
            self.__tree.delete(item)

        # Fetch records from the API
        records = self.__api.fetch_records()
        if records:
            for record in records:

                generacion = record.get('generacion', 'N/A')
                spartan = record.get('spartan', 'N/A')
                apellido = record.get('apellido', 'N/A')
                ciudad = record.get('ciudad', 'N/A')
                colonia = record.get('colonia', 'N/A')


                self.__tree.insert("", "end", values=(generacion, spartan, apellido, ciudad, colonia))

            # Display a random record if available
            random_record = self.__api.fetch_random_record()
            if random_record:
                messagebox.showinfo(
                    "Registro Aleatorio",
                    f"Registro Aleatorio:\nGeneración: {random_record.get('generacion', 'N/A')}\n"
                    f"Spartan: {random_record.get('spartan', 'N/A')}\nApellido: {random_record.get('apellido', 'N/A')}\n"
                    f"Ciudad: {random_record.get('ciudad', 'N/A')}\nColonia: {random_record.get('colonia', 'N/A')}"
                )
        else:
            messagebox.showwarning("Advertencia", "No se pudieron cargar los registros.")

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
        tk.Label(detail_window, text="Colonia: " + record.get('colonia', 'N/A')).pack(pady=10)
