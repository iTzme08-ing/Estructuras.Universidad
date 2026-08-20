from Ejercicio19.persona import persona
from Ejercicio19.titulo import titulo
class docente(persona):
    def __init__(self, nombre, documento,asignatura):
        super().__init__(nombre, documento)
        self.asignatura=asignatura
        self.lista_recursos=[]
        self.estudios=[]

    def solicitar_recurso(self,recurso):
        self.lista_recursos.append(recurso)

    def recorrer_recursos(self):
        for x in self.lista_recursos:
            print(x.get_recurso())

    def asignar_estudio(self,nivel_t,nombre_t):
        t1=titulo(nivel_t,nombre_t)
        self.estudios.append(t1)