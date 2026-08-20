class persona:
    def __init__(self, nombre,documento):
        self.nombre=nombre
        self.documento=documento
    def ver_datos(self):
        return f"nombre:{self.nombre} documento:{self.documento}"