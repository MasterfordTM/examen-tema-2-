import tkinter as tk
from tkinter import ttk, messagebox
import requests
import random

class API:
    def __init__(self, base_url):
        self.__base_url = base_url

    def fetch_records(self):
        response = requests.get(self.__base_url)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def fetch_random_record(self):
        records = self.fetch_records()
        if records:
            return random.choice(records)
        return None

    def fetch_record_by_id(self, record_id):
        records = self.fetch_records()
        for record in records:
            if str(record['id']) == str(record_id):
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

        self.__tree = ttk.Treeview(self, columns=("ID", "Nombre", "Apellido", "Ciudad", "Calle"), show="headings")
        self.__tree.heading("ID", text="ID")
        self.__tree.heading("Nombre", text="Nombre")
        self.__tree.heading("Apellido", text="Apellido")
        self.__tree.heading("Ciudad", text="Ciudad")
        self.__tree.heading("Calle", text="Calle")
        self.__tree.pack(expand=True, fill='both')

        self.__input_button = tk.Button(self, text="Buscar Registro por ID", command=self.__input_record_id)
        self.__input_button.pack(pady=10)

    def __load_records(self):

        for item in self.__tree.get_children():
            self.__tree.delete(item)


        records = self.__api.fetch_records()
        if records:

            for record in records:
                self.__tree.insert("", "end", values=(record['id'], record['nombre'], record['apellido'], record['ciudad'], record['calle']))


            random_record = self.__api.fetch_random_record()
            if random_record:
                messagebox.showinfo("Registro Aleatorio", f"Registro Aleatorio:\nID: {random_record['id']}\nNombre: {random_record['nombre']}\nApellido: {random_record['apellido']}\nCiudad: {random_record['ciudad']}\nCalle: {random_record['calle']}")
        else:
            messagebox.showwarning("Advertencia", "No se pudieron cargar los registros.")

    def __input_record_id(self):
        input_window = tk.Toplevel(self)
        input_window.title("Buscar Registro por ID")
        input_window.geometry("300x150")

        tk.Label(input_window, text="Ingrese el ID del registro:").pack(pady=10)
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
            messagebox.showwarning("Advertencia", "Por favor, ingrese un ID válido.")
        input_window.destroy()

    def __show_record_details(self, record):
        detail_window = tk.Toplevel(self)
        detail_window.title("Detalles del Registro de Usuario")
        detail_window.geometry("600x400")

        tk.Label(detail_window, text="ID: " + str(record['id'])).pack(pady=20)
        tk.Label(detail_window, text="Nombre: " + record['nombre']).pack(pady=10)
        tk.Label(detail_window, text="Apellido: " + record['apellido']).pack(pady=10)
        tk.Label(detail_window, text="Ciudad: " + record['ciudad']).pack(pady=10)
        tk.Label(detail_window, text="Calle: " + record['calle']).pack(pady=10)

