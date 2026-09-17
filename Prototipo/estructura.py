"""Lista circular ordenada por prioridad para las solicitudes."""

from __future__ import annotations                  #Facilita las referencias de tipo en clases que se apuntan a sí mismas (Nodo)
                                                    #sin cambiar la lógica de la lista
from dataclasses import dataclass

from Prototipo.solicitud import Solicitud


@dataclass
class Nodo:
    dato: Solicitud
    siguiente: Nodo | None = None                   #El nodo guarda una solicitud y un puntero al siguiente nodo, 
                                                    #que puede ser otro nodo o None si aún no está enlazado.
                                                    #Se inicia en None para indicar que no tiene un siguiente nodo al crearlo.
class ListaPrioridadCircular:
    def __init__(self) -> None:
        self.primero: Nodo | None = None
        self.ultimo: Nodo | None = None
        self.actual: Nodo | None = None
        self.tamano = 0                                                             #Cuantos nodos hay en la lista, inicia en 0 porque la lista está vacía al crearla.
        self._siguiente_id = 1                                                      #Guarda el ID que se asgina a la solicitud
        # Para cada prioridad guarda el ID que debe receive el próximo turno.
        self._proximo_por_prioridad: dict[int, int] = {}

    def __len__(self) -> int:           #Devuelve el número de solicitudes en la lista.
        return self.tamano

    def esta_vacia(self) -> bool:           #Devuelve True si la lista está vacía, False en caso contrario.
        return self.primero is None

    def insertar(self, solicitud: Solicitud) -> int:
        if solicitud.id_solicitud is None:
            solicitud.id_solicitud = self._siguiente_id         #Inserta una solicitud en la lista, asigna un ID y la ubica según su prioridad
            self._siguiente_id += 1                             #manteniendo el orden de llegada cuando hay empates.

        nuevo = Nodo(solicitud)
        if self.esta_vacia():
            nuevo.siguiente = nuevo                                 
            self.primero = self.ultimo = self.actual = nuevo
            self.tamano = 1
            return solicitud.id_solicitud

        assert self.primero is not None and self.ultimo is not None
        if solicitud.prioridad() > self.primero.dato.prioridad():
            nuevo.siguiente = self.primero
            self.primero = nuevo
            self.ultimo.siguiente = nuevo
        else:
            cursor = self.primero
            while cursor.siguiente is not self.primero and cursor.siguiente.dato.prioridad() >= solicitud.prioridad():
                cursor = cursor.siguiente
            nuevo.siguiente = cursor.siguiente
            cursor.siguiente = nuevo
            if cursor is self.ultimo:
                self.ultimo = nuevo

        self.tamano += 1
        if solicitud.es_emergencia:                         #Una urgencia crítica interrumpe la rotación actual. Para las demás
            self.actual = nuevo                             #solicitudes se conserva el orden de rotación entre los empates.
        else:
            self._actualizar_turno()
        return solicitud.id_solicitud

    def buscar(self, id_solicitud: int) -> Solicitud | None:
        nodo, _ = self._buscar_nodo(id_solicitud)               #Localiza una solicitud por su ID
        return nodo.dato if nodo else None                      #y la devuelve si existe; si no, devuelve None

    def actualizar(self, id_solicitud: int, **cambios: object) -> bool:
        solicitud = self.buscar(id_solicitud)
        if solicitud is None:
            return False
        nueva = Solicitud(                                                      #Valida y reinserta una solicitud para mantener el orden de prioridad.
            cambios.get("municipio", solicitud.municipio),
            cambios.get("nivel_urgencia", solicitud.nivel_urgencia),
            cambios.get("vulnerable", solicitud.vulnerable),
            cambios.get("tiempo_espera", solicitud.tiempo_espera),
        )
        nueva.id_solicitud = id_solicitud
        era_turno_actual = self.actual is not None and self.actual.dato.id_solicitud == id_solicitud
        self.eliminar(id_solicitud)
        self.insertar(nueva)
        if era_turno_actual:
            self._actualizar_turno()
        return True

    def eliminar(self, id_solicitud: int) -> Solicitud | None:
        nodo, anterior = self._buscar_nodo(id_solicitud)
        if nodo is None:
            return None
        assert self.primero is not None and self.ultimo is not None
        if self.tamano == 1:
            self.primero = self.ultimo = self.actual = None
        else:
            assert anterior is not None and nodo.siguiente is not None              #busca una solicitud por su ID, la elimina de la lista
            anterior.siguiente = nodo.siguiente                                     #y ajusta los enlaces y turno para mantener la estructura correcta.
            if nodo is self.primero:
                self.primero = nodo.siguiente
            if nodo is self.ultimo:
                self.ultimo = anterior
            self.ultimo.siguiente = self.primero
            if nodo is self.actual:
                self.actual = nodo.siguiente
        self.tamano -= 1
        nodo.siguiente = None
        self._actualizar_turno()
        return nodo.dato

    def pasar_turno(self) -> Solicitud | None:
        if self.actual is None:
            return None
        atendida = self.actual.dato
        siguiente = self._siguiente_con_prioridad(self.actual, atendida.prioridad())            #Rota entre solicitudes con la prioridad máxima actual.
        if siguiente is not None:                                                               #Sin eliminar sin el turno
            self._proximo_por_prioridad[atendida.prioridad()] = siguiente.dato.id_solicitud
        self._actualizar_turno()
        return atendida

    def resolver_turno_actual(self) -> Solicitud | None:
        if self.actual is None:
            return None
        atendida = self.actual.dato
        siguiente = self._siguiente_con_prioridad(self.actual, atendida.prioridad())              #Rota entre solicitudes con la prioridad máxima actual.
        if siguiente is not None and siguiente is not self.actual:                                #Eliminando el turno
            self._proximo_por_prioridad[atendida.prioridad()] = siguiente.dato.id_solicitud
        return self.eliminar(atendida.id_solicitud)

    def solicitudes(self, desde_turno_actual: bool = False) -> list[Solicitud]:
        if self.primero is None:
            return []
        if desde_turno_actual:
            return self._turnos_programados()

        inicio = self.primero
        resultado: list[Solicitud] = []
        nodo = inicio
        while True:
            resultado.append(nodo.dato)
            assert nodo.siguiente is not None
            nodo = nodo.siguiente
            if nodo is inicio:
                return resultado

    def _turnos_programados(self) -> list[Solicitud]:                   
        assert self.actual is not None
        resultado: list[Solicitud] = []                     #Muestra primero toda la ronda de la prioridad que está en turno.
        ids_incluidos: set[int] = set()
        prioridad = self.actual.dato.prioridad()
        nodo = self.actual
        while True:
            resultado.append(nodo.dato)
            ids_incluidos.add(nodo.dato.id_solicitud)
            siguiente = self._siguiente_con_prioridad(nodo, prioridad)
            if siguiente is None or siguiente is self.actual:
                break
            nodo = siguiente

        # Las prioridades inferiores quedan después de completar esa ronda.
        for solicitud in self.solicitudes():
            if solicitud.id_solicitud not in ids_incluidos:
                resultado.append(solicitud)
        return resultado

    def _buscar_nodo(self, id_solicitud: int) -> tuple[Nodo | None, Nodo | None]:
        if self.primero is None:
            return None, None
        anterior = self.ultimo
        nodo = self.primero
        while True:
            if nodo.dato.id_solicitud == id_solicitud:
                return nodo, anterior
            anterior, nodo = nodo, nodo.siguiente
            assert nodo is not None
            if nodo is self.primero:
                return None, None

    def _actualizar_turno(self) -> None:
        if self.primero is None:                    #Selecciona el turno de mayor prioridad y respeta sus empates
            self.actual = None
            return

        prioridad_maxima = self.primero.dato.prioridad()
        id_preferido = self._proximo_por_prioridad.get(prioridad_maxima)
        if id_preferido is not None:
            nodo_preferido, _ = self._buscar_nodo(id_preferido)
            if nodo_preferido is not None and nodo_preferido.dato.prioridad() == prioridad_maxima:
                self.actual = nodo_preferido
                return

        # Al no haber un empate pendiente, inicia por el primero del grupo.
        self.actual = self.primero

    def _siguiente_con_prioridad(self, nodo_inicio: Nodo, prioridad: int) -> Nodo | None:
        if self.primero is None:
            return None
        assert nodo_inicio.siguiente is not None
        nodo = nodo_inicio.siguiente
        while True:                                               #Busca, en sentido circular, el siguiente nodo de una prioridad dada
            if nodo.dato.prioridad() == prioridad:
                return nodo
            assert nodo.siguiente is not None
            nodo = nodo.siguiente
            if nodo is nodo_inicio:
                return None
