"""Modelo de una solicitud de atención municipal."""

from dataclasses import dataclass, field  # "dataclass" Decorador para crear clases de datos, ahorra construir el metodo constructo
                                          # "field" Permite definir atributos de la clase con opciones adicionales
                                            # por ejemplo en la linea 16, crea el atributo, que empiece en None y no lo genera al momento de crear la solicitud.

LIMITE_ESPERA = 48  # horas


@dataclass
class Solicitud:
    municipio: str
    nivel_urgencia: int
    vulnerable: bool = False
    tiempo_espera: int = 0
    id_solicitud: int | None = field(default=None, init=False)  #Indica que si no se asigna un valor, empieza en None. 
                                                                #Python espera que le pases un id al crear la solicitud.
                                                                #Evita que se lo pidas al usuario cuando creas la solicitud.

    def __post_init__(self) -> None:
        self.municipio = self.municipio.strip()                 #Quita espacios en blanco al inicio y al final del municipio, para evitar errores de validación.
        if not self.municipio:
            raise ValueError("El municipio no puede estar vacío.")
        if not isinstance(self.nivel_urgencia, int) or not 1 <= self.nivel_urgencia <= 5:
            raise ValueError("El nivel de urgencia debe ser un entero entre 1 y 5.")             #Despues de crear el objeto "Solicitud"
        if not isinstance(self.vulnerable, bool):                                                #valida que los atributos cumplan con las condiciones.
            raise ValueError("El campo vulnerable debe ser verdadero o falso.")
        if not isinstance(self.tiempo_espera, int) or self.tiempo_espera < 0:
            raise ValueError("El tiempo de espera debe ser un entero no negativo.")

    @property
    def es_emergencia(self) -> bool:                                #Una urgencia de nivel 5 tiene atención inmediata
        return self.nivel_urgencia == 5

    def prioridad(self) -> int:
        bono_equidad = 2 if self.vulnerable and self.tiempo_espera > LIMITE_ESPERA else 0
        return self.nivel_urgencia + bono_equidad

    def __str__(self) -> str:                                                               #Metodo que convierte el objeto en texto legible
        identificador = self.id_solicitud if self.id_solicitud is not None else "-"         #El identificador se muestra como "-", hasta que se le asigne un valor, 
        return (                                                                            #que se hace cuando se inserta en la lista de prioridad circular.
            f"ID: {identificador:>3} | Municipio: {self.municipio:15.15} | "
            f"Urgencia: {self.nivel_urgencia} | "
            f"Vulnerable: {'Sí' if self.vulnerable else 'No':3} | "
            f"Espera: {self.tiempo_espera:>3} h | Prioridad: {self.prioridad()}"
        )
