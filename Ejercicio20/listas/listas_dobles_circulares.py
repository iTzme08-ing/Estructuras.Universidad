class nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class lista_doble_circular:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def append(self, dato):
        nuevo = nodo(dato)

        if self.cabeza is None:
            # Si es el primer nodo, apunta hacia sí mismo
            self.cabeza = nuevo
            self.cola = nuevo
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo

        else:
            # Conectar el nuevo nodo con la cola
            nuevo.anterior = self.cola
            nuevo.siguiente = self.cabeza

            # Conectar la cola actual con el nuevo nodo
            self.cola.siguiente = nuevo

            # Conectar la cabeza con el nuevo nodo
            self.cabeza.anterior = nuevo

            # Actualizar la cola
            self.cola = nuevo

    def forward(self):
        if self.cabeza is None:
            return

        actual = self.cabeza

        while True:
            print(actual.dato)
            actual = actual.siguiente

            # Cuando vuelve a la cabeza, termina
            if actual == self.cabeza:
                break


milista_doble = lista_doble_circular()

milista_doble.append(100)
milista_doble.append(120)
milista_doble.append(80)
milista_doble.append(9)

milista_doble.forward()