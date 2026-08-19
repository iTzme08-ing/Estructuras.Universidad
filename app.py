from recurso import recurso
from docente import docente

r1 = recurso("Computadora")
r2 = recurso("Proyector")
r3 = recurso("Libro")

d1 = docente("Juan", "123456", "Matematicas")

d1.solicitar_recurso(r1)
d1.solicitar_recurso(r2)
d1.solicitar_recurso(r3)

print("Recursos asignados al docente:")
print(d1.ver_recursos_asignados())