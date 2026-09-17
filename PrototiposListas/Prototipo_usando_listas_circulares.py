LIMITE_ESPERA = 48  # horas límite de espera (equidad territorial)


class Solicitud:
    """
    Objeto que representa la petición de un municipio.
    nivel_urgencia: 1 (baja) a 5 (crítica / salto de emergencia)
    vulnerable: True si es un municipio pequeño, vulnerable o alejado
    tiempo_espera: horas que lleva esperando la solicitud
    """

    def __init__(self, municipio, nivel_urgencia, vulnerable=False, tiempo_espera=0):
        self.municipio = municipio
        self.nivel_urgencia = nivel_urgencia
        self.vulnerable = vulnerable
        self.tiempo_espera = tiempo_espera

    def prioridad(self):
        # Bono de equidad territorial
        bono = 2 if (
            self.vulnerable and self.tiempo_espera > LIMITE_ESPERA
        ) else 0

        return self.nivel_urgencia + bono

    def __str__(self):
        return (
            f"Municipio: {self.municipio:12} | "
            f"Urgencia: {self.nivel_urgencia} | "
            f"Vulnerable: {'Sí' if self.vulnerable else 'No':3} | "
            f"Espera: {self.tiempo_espera:3}h | "
            f"Prioridad final: {self.prioridad()}"
        )


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaPrioridadCircular:

    def __init__(self):
        self.primero = None

        # MODIFICACIÓN 1:Se agrega "ultimo" para poder conectar el último nodo nuevamente con el primero.

        self.ultimo = None

        # MODIFICACIÓN 2:Se agrega "actual" para controlar el turno de atención y permitir la rotación de los municipios.

        self.actual = None

    def insertar(self, dato):
        nuevo = Nodo(dato)

        # MODIFICACIÓN 3: CASO DE LISTA VACÍA

        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo

            # CIRCULARIZACIÓN DE LA LISTA
            # Como solo existe un nodo, hacemos que su enlace
            # "siguiente" apunte hacia él mismo.
            #
            # En una lista normal sería:
            #
            #     nuevo.siguiente = None
            #
            # En una lista circular:
            #
            #     nuevo.siguiente = nuevo
            #
            # Esto hace que el recorrido pueda volver al
            # mismo nodo y no termine en None.

            nuevo.siguiente = nuevo

            # El primer turno comienza en este municipio.
            
            self.actual = nuevo

            return

        # SALTO DE EMERGENCIA
        # Esta lógica ya existía en la lista original, pero se adapta para conservar la circularidad.

        if dato.prioridad() > self.primero.dato.prioridad():

            nuevo.siguiente = self.primero
            self.primero = nuevo

            # MODIFICACIÓN 4:CIRCULARIZACIÓN DESPUÉS DE INSERTAR AL INICIO

            self.ultimo.siguiente = self.primero

            return

        # INSERTAR EN LA POSICIÓN CORRESPONDIENTE

        actual = self.primero

        # MODIFICACIÓN 5: CONDICIÓN DEL RECORRIDO
        # 
        # En la lista original se utilizaba:
        #
        #     while actual.siguiente and ...
        #
        # porque la lista terminaba en None.
        #
        # Ahora debemos detenernos cuando el siguiente nodo
        # sea nuevamente el primero.

        while (actual.siguiente != self.primero
                    and actual.siguiente.dato.prioridad() >= dato.prioridad()):
            actual = actual.siguiente

        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo

        # MODIFICACIÓN 6: Si la nueva solicitud se inserta después del último nodo, ahora ese nuevo nodo pasa a ser el último.

        if actual == self.ultimo:
            self.ultimo = nuevo

        # CIRCULARIZACIÓN DE LA LISTA: El nuevo último nodo debe apuntar nuevamente al primer nodo.

        self.ultimo.siguiente = self.primero

    def atender(self):
        """
        Atiende el municipio que está en el turno actual
        y mueve el turno al siguiente municipio.

        Al llegar al último municipio, automáticamente
        vuelve al primero.
        """

        if self.actual is None:
            print("No hay solicitudes para atender.")
            return

        print("\n=== ATENDIENDO SOLICITUD ===")
        print(self.actual.dato)

        # MODIFICACIÓN 7: ROTACIÓN DEL TURNO En lugar de finalizar cuando se llega al último nodo, se avanza al siguiente.

        self.actual = self.actual.siguiente

        print(f"\nSiguiente turno: {self.actual.dato.municipio}")

    def mostrar(self):
        if self.primero is None:
            print("No hay solicitudes en la fila.")
            return

        print("\n=== FILA INTELIGENTE DE TURNOS - GOBERNACIÓN ===")

        actual = self.primero
        posicion = 1

        # ==================================================
        # MODIFICACIÓN 8 RECORRIDO DE UNA LISTA CIRCULAR: En la lista original se utilizaba "while actual:" porque el último nodo apuntaba a None. Ahora eso produciría un recorrido infinito.
        # Por eso utilizamos while True y detenemos el recorrido cuando volvemos al nodo primero.

        while True:
            print(f"{posicion}. {actual.dato}")

            actual = actual.siguiente
            posicion += 1

            # CIRCULARIZACIÓN / FINAL DEL RECORRIDO

            if actual == self.primero:
                break

    def mostrar_desde_turno_actual(self):
        """
        Muestra la fila comenzando desde el turno actual.
        """

        if self.actual is None:
            print("No hay solicitudes en la fila.")
            return

        print("\n=== ROTACIÓN ACTUAL DE TURNOS ===")

        inicio = self.actual
        actual = inicio
        posicion = 1

        # MODIFICACIÓN 9:
        # RECORRIDO CIRCULAR DESDE EL TURNO ACTUAL

        while True:
            print(f"{posicion}. {actual.dato}")

            actual = actual.siguiente
            posicion += 1

            # Se detiene cuando vuelve al punto donde comenzó.
            if actual == inicio:
                break


if __name__ == "__main__":

    fila = ListaPrioridadCircular()

    fila.insertar(
        Solicitud(
            "San José",
            nivel_urgencia=2,
            vulnerable=True,
            tiempo_espera=60
        )
    )

    fila.insertar(
        Solicitud(
            "La Capital",
            nivel_urgencia=5,
            vulnerable=False,
            tiempo_espera=5
        )
    )

    fila.insertar(
        Solicitud(
            "El Retiro",
            nivel_urgencia=1,
            vulnerable=False,
            tiempo_espera=10
        )
    )

    fila.insertar(
        Solicitud(
            "Guacarí",
            nivel_urgencia=3,
            vulnerable=True,
            tiempo_espera=50
        )
    )

    fila.insertar(
        Solicitud(
            "Alerta Roja",
            nivel_urgencia=5,
            vulnerable=False,
            tiempo_espera=0
        )
    )

    # Mostrar la fila completa
    fila.mostrar()

    # PRUEBA DE ROTACIÓN DE TURNOS

    print("\n\n=== PRUEBA DE ROTACIÓN ===")

    fila.atender()
    fila.atender()
    fila.atender()
    fila.atender()
    fila.atender()
    fila.atender()
    fila.atender()