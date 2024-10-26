import tkinter as tk
from tkinter import ttk, messagebox

import requests

class API:
    def __init__(self, base_url):
        self.__base_url = base_url
    def fetch_records(self):
        response = requests.get(self.__base_url)
        if response.status_code == 200:
            return response.json()
        else:
            return []

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

        self.__select_button = tk.Button(self, text="Seleccionar Registro", command=self.__select_record)
        self.__select_button.pack(pady=10)

        self.__show_button = tk.Button(self, text="Mostrar Registro Seleccionado", command=self.__show_selected_record)
        self.__show_button.pack(pady=10)

    def __load_records(self):
        records = self.__api.fetch_records()
        for record in records:
            self.__tree.insert("", "end", values=(record['id'], record['nombre'], record['apellido'], record['ciudad'], record['calle']))

    def __select_record(self):
        selected_item = self.__tree.selection()
        if selected_item:
            item_data = self.__tree.item(selected_item)
            print("Registro seleccionado:", item_data['values'])

    def __show_selected_record(self):
        selected_item = self.__tree.selection()
        if selected_item:
            item_data = self.__tree.item(selected_item)
            record = item_data['values']
            self.__show_record_details(record)
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un registro primero.")

    def __show_record_details(self, record):
        detail_window = tk.Toplevel(self)
        detail_window.title("Detalles del Registro de Usuario")
        detail_window.geometry("600x600")

        tk.Label(detail_window, text="ID: " + str(record[0])).pack(pady=5)
        tk.Label(detail_window, text="Nombre: " + record[1]).pack(pady=5)
        tk.Label(detail_window, text="Apellido: " + record[2]).pack(pady=5)
        tk.Label(detail_window, text="Ciudad: " + record[3]).pack(pady=5)
        tk.Label(detail_window, text="Calle: " + record[4]).pack(pady=5)





