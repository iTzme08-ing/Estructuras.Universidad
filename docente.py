from persona import persona

#Docente hereda de persona "Es una persona"
#Docente tiene una asignatura y un recurso "Tiene un..."

class docente(persona):
    def __init__(self, nombre, documento, asignatura):
        super().__init__(nombre, documento)
        self.asignatura = asignatura
        self.lista_recursos = []

    def solicitar_recurso(self, recurso):
        self.lista_recursos.append(recurso)

    def ver_recursos_asignados(self):
        return [recurso.get_recursos() for recurso in self.lista_recursos]