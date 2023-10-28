# Supongamos que el tamaño máximo de ventana es 16 en LZ utilizado actualmente, entonces se requiere de 5 bits
#para expresar el valor 16
import math

VENTANA = 2
VENTANA_MAX_BITS = int(math.log2(VENTANA)+1)
TXT = "../datos/texto1.txt.bwt"
