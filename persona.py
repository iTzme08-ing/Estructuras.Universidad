class persona:
    def __init__(self, nombre, documento):
        self.nombre = nombre
        self.documento = documento
    def ver_datos(self):
        print(f"Nombre: {self.nombre}")
        print(f"Documento: {self.documento}")