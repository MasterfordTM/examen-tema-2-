from tkinter import ttk


class RecordTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent, columns=(
        "generacion", "spartan", "apellido", "ciudad", "planteldeentrenamiento", "estadodemision"), show="headings")

        self.heading("generacion", text="Generación")
        self.heading("spartan", text="Spartan")
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