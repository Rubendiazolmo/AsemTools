import os
import xml.etree.ElementTree as ET
import sys

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
    
input("Pulse ENTER para finalizar")
sys.exit()
print("Archivos no revisados")
for Archivo in list(set(ArchivosNoRevisados)):
    print(f' - {Archivo}')
    
