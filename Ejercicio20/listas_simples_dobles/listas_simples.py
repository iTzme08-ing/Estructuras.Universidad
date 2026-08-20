class nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class lista:
    def __init__(self):
        self.primero = None

    def append(self, dato):
        nuevo=nodo(dato)
        if self.primero is None:
            self.primero=nuevo
        else:
            actual=self.primero
            while actual.siguiente:
                actual=actual.siguiente
            actual.siguiente=nuevo

    def mostrar(self):
        actual=self.primero
        while actual:
            print(actual.dato)
            actual=actual.siguiente


milista=lista()
milista.append(100)
milista.append(50)
milista.append(1000)
milista.append(25)
milista.mostrar()