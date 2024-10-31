from tkinter import ttk
from ull import  API


class RecordTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent, columns=(
        "generacion", "espartano", "apellido", "ciudad", "planteldeentrenamiento", "estadodemision"), show="headings")

        self.api = API #mi referencia a la clase api
        self.current_records = [] # comparar mis nuevos regitrso con los anterirorees
        self.pack(expand=True, fill='both') # posiciones

        self.heading("generacion", text="Generación")
        self.heading("espartano", text="espartano")
        self.heading("apellido", text="Apellido")
        self.heading("ciudad", text="Ciudad")
        self.heading("planteldeentrenamiento", text="Plantel de Entrenamiento")
        self.heading("estadodemision", text="Estado")

        self.pack(expand=True, fill='both')

    def load_records(self, records):
        for item in self.get_children():
            self.delete(item)

        for record in records:
            generacion = record.get('generacion', 'N/A')
            spartan = record.get('spartan', 'N/A')
            apellido = record.get('apellido', 'N/A')
            ciudad = record.get('ciudad', 'N/A')
            planteldeentrenamiento = record.get('planteldeentrenamiento', 'N/A')
            estadodemision = record.get('estadodemision', 'N/A')

            self.insert("", "end",
                        values=(generacion, spartan, apellido, ciudad, planteldeentrenamiento, estadodemision))


    def registros_nuevos(self):
        new_records = self.api.get_records()
        if new_records != self.current_records:
            self.load_records(new_records)
            self.current_records = new_records
        self.after(5000, self.registros_nuevos)
