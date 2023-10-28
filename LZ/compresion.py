import math
from descompresion import descomprimir
from variables_globales import VENTANA,VENTANA_MAX_BITS,TXT
from movimiento import movimiento_ventana
def match(bytes_ventana,bytes_no_comprimidos):

    if bytes_ventana.find(bytes_no_comprimidos) != -1:
        return bytes_no_comprimidos

    return bytearray()
def comprimido_bytes(comprimido_bin):
    while len(comprimido_bin) % 8 != 0:
        comprimido_bin = comprimido_bin + '0'

    arr_bytes=bytes([int(comprimido_bin[i:i+8], 2) for i in range(0, len(comprimido_bin), 8)])
    return arr_bytes
def comprimir():
    try:
        archivo = open(TXT, 'rb')

        # Primero codificamos en 4 bits el valor "n < 16" que es el tamaño de la ventana, para que el receptor
        # luego pueda decodificar
        comprimido = bin(VENTANA)[2:].zfill(VENTANA_MAX_BITS)
        procesado=bytearray(archivo.read(VENTANA))
        ventana_lectura=bytearray()
        # Llenamos la ventana y la codificamos
        # Luego en la lectura sabremos n° de bits iniciales que solo expresan los codigos de los "simbolos"
        # cargados en la ventana, porque ya con los primeros bits sabemos el tamaño de la ventana, siendo un total
        # "log2(VENTANA)"
        if len(procesado)!=VENTANA:
            return "" #Fin del archivo
        else:
            for i in range(VENTANA):
                ventana_lectura.append(procesado[i])
                simb = bin(ventana_lectura[i])[2:].zfill(8)
                comprimido = comprimido + simb

        print("\nLos primeros \""+ str(VENTANA) +"\" simbolos de la ventana: " + str(ventana_lectura)+"\n")

        long_fuente=VENTANA
        aux = archivo.read(1)
        if not aux:
            return "" #Fin del archivo
        procesado.append(aux[0])
        pos_byte=VENTANA

        while True:
            #print(str(ventana_lectura))
            cadena_match=bytearray()

            while len(match(ventana_lectura,procesado[pos_byte:]))!=0 and len(cadena_match) < VENTANA:
                cadena_match.append(procesado[pos_byte + len(cadena_match)])
                aux = archivo.read(1)
                if not aux:
                    break #Fin del archivo
                procesado.append(aux[0])

            # Quiere decir que hay coincidencia, aunque sea de longitud 1
            if(len(cadena_match) > 0):

                # flag = 0 + posicion_coincidencia expresada en log2(ventana) bits + long_coincidencia expresada en log2(ventana) + 1 bits
                simb = '0' + bin(ventana_lectura.index(cadena_match[0]))[2:].zfill(int(math.log2(VENTANA))) + bin(len(cadena_match))[2:].zfill(int(math.log2(VENTANA) + 1))
                ventana_lectura=movimiento_ventana(ventana_lectura,procesado,len(cadena_match),pos_byte)
                pos_byte+= len(cadena_match)
            else:
                #Si no coincide le sumo 1 a pos_byte, si hay coincidencia le sumo len(cadena_match) entonces siempre apunta
                #al siguiente de la ventana, es decir, el ultimo procesado
                aux = archivo.read(1)
                if not aux:
                    break #Fin del archivo
                procesado.append(aux[0])

                # flag = 1 + codPseudo = (1 + long_codigo) bits
                simb = '1' + bin(procesado[pos_byte])[2:].zfill(8)
                ventana_lectura=movimiento_ventana(ventana_lectura,procesado,len(cadena_match),pos_byte)
                pos_byte+= 1

            comprimido = comprimido + simb
            #print("cadena que hizo match: " + cadena_match)

        long_fuente=pos_byte
        #print("\nOriginal (Bytes): "+ str(procesado))
        print("\nLongitud del original: "+str(long_fuente*8)+" bits")

        return comprimido_bytes(comprimido)

    except FileNotFoundError:
        print(f"El archivo no se encontró.")
    except Exception as e:
        print(f"Se produjo un error: {str(e)}")
def main():
    comprimido = comprimir()
    if comprimido != "":
        #print("\n\nComprimido (Bytes): "+ str(comprimido))
        print("\n\nLongitud de Comprimido (Incluyendo 4 bits para tamaño de ventana): "+str(len(comprimido)*8)+" bits")
        print("\n\nLa longitud del descomprimido: " + str(len(descomprimir(comprimido))*8)+" bits")

    else:
        print("\n\nVENTANA DEMASIADO GRANDE PARA COMPRIMIR")

if __name__ == '__main__':
    main()