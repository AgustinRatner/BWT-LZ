# Supongamos que el tamaño máximo de ventana es 16 en LZ utilizado actualmente, entonces se requiere de 5 bits
#para expresar el valor 16
import math

VENTANA = 4
VENTANA_MAX_BITS = int(math.log2(VENTANA)+1)
ORIGEN = "../datos/agu.jpg"
DESTINO = "../datos/agu1.jpg"
