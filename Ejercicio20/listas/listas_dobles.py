class nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class lista_doble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def append(self, dato):
        nuevo = nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            nuevo.anterior = self.cola
            self.cola = nuevo

    def forward(self):
        actual = self.cabeza
        while actual:
            print(actual.dato)
            actual = actual.siguiente

milista_doble = lista_doble()
milista_doble.append(100)
milista_doble.append(120)
milista_doble.append(80)
milista_doble.append(9)
milista_doble.forward()