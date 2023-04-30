# coding=<UTF-16>

import os
import xml.etree.ElementTree as ET
import sys
import re

def VarSinUsar():

    # definir varibles auxiliares
    VarUsada            = False  # Auxiliar variable encontrada para salir del bucle
    ArchivosNoRevisados = list() # LLista de archivos no revisado por error al leerlo
    VarSinUsar          = list() # Lista variables sin usar
    ListaVar            = list() # Lista varible

    # Obtener archivo de variables

    extension = ".hmirealtimedb"  # extensión deseada
    archivos = os.listdir(".")    # lista de todos los archivos en el directorio actual

    # Filtrar archivos con la extensión deseada
    archivos_con_extension = [archivo for archivo in archivos if archivo.endswith(extension)]

    # Obtener el nombre del primer archivo con la extensión deseada (si existe)
    RutaArchivoVar = archivos_con_extension[0]

    # definir la propiedad que queremos buscar
    NombreProp = 'Variable'

    # analizar el archivo XML y encontrar todos los hijos de la propiedad
    xml_tree = ET.parse(RutaArchivoVar)
    root     = xml_tree.getroot()

    for variable in root.iter(NombreProp):          # Extraer todos los elementos de tipo "Variable" del archivo de alarmas
        ListaVar.append(variable.find('Name').text) # Extraer los nombres de las variables

    # Compruebo en todos los archivos del proyecto si se utiliza alguna variable (los fors para buscar todos los archivos está fusilado de internet)
    for Var in ListaVar:
        VarUsada = False
        for dirpath, dirnames, filenames in os.walk(os.getcwd()):
            if VarUsada:
                continue
            for filename in filenames:
                if filename != RutaArchivoVar:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        file = open(file_path, 'r', encoding="UTF-16")
                        for linea in file:
                            if Var in linea:
                                VarUsada = True
                                continue
                            
                    except Exception as e:
                        ArchivosNoRevisados.append(filename)
        if not VarUsada:
            VarSinUsar.append(Var)

    print("Variales sin usar:")
    for Var in VarSinUsar:
        print(f' - {Var}')
        
    if len(ArchivosNoRevisados) > 0:
        print("Ha habido archivos que no se han podido revisar")
        rsp = input("¿Quieres verlos? (s/n)? ").lower()
        if rsp == "s":
            for Archivo in list(set(ArchivosNoRevisados)):
                print(f' - {Archivo}')
            input("Pulse ENTER para finalizar")

def ImagenesSinUsar():
    # definir Imagenibles auxiliares
    ImagenUsada             = False  # Auxiliar Imageniable encontrada para salir del bucle
    ArchivosNoRevisados     = list() # LLista de archivos no revisado por error al leerlo
    ImagenesSinUsar         = list() # Lista Imageniables sin usar
    ListaImagen             = list() # Lista Imagenible

    # Obtener la lista de archivos en el subdirectorio "imagenes"
    ListaImagen = os.listdir("./IMAGES")

    # Compruebo en todos los archivos del proyecto si se utiliza alguna Imageniable (los fors para buscar todos los archivos está fusilado de internet)
    for Imagen in ListaImagen:
        ImagenUsada = False
        for dirpath, dirnames, filenames in os.walk(os.getcwd()):
            if ImagenUsada:
                continue
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    file = open(file_path, 'r', encoding="UTF-16")
                    for linea in file:
                        if Imagen in linea:
                            ImagenUsada = True
                            continue
                        
                except Exception as e:
                    ArchivosNoRevisados.append(filename)
        if not ImagenUsada:
            ImagenesSinUsar.append(Imagen)

    print("Imagenes sin usar:")
    for Imagen in ImagenesSinUsar:
        print(f' - {Imagen}')

    if len(ArchivosNoRevisados) > 0:
        print("Ha habido archivos que no se han podido revisar")
        rsp = input("¿Quieres verlos? (s/n)? ").lower()
        if rsp == "s":
            for Archivo in list(set(ArchivosNoRevisados)):
                print(f' - {Archivo}')
            input("Pulse ENTER para finalizar")

print("Selecciona la utlidad a ejecutar: ")
print("1: Listar variables sin usar")
print("2: Listar imágenes sin usar")

UtilidadAEjecutar = int(input(""))

os.system("cls")

if UtilidadAEjecutar == 1:
    VarSinUsar()
if UtilidadAEjecutar == 2:
    ImagenesSinUsar() 