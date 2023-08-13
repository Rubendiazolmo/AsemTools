import re
import subprocess
import os
import xml.etree.ElementTree as ET

# Obtener variables definidas

# definir varibles auxiliares
VarDefinidas = list() # Lista varible

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
    VarDefinidas.append(variable.find('Name').text) # Extraer los nombres de las variables


output = subprocess.check_output("dir *.hmiscr /b /s /A-D ", shell=True).decode()

Pdls = (output.split("\r\n"))

for Pdl in Pdls:
    Variables = list()
    try:
        with open(Pdl, "r", encoding="UTF-16") as file:

            XML_Pdl = file.read()

            # Expresión regular para encontrar patrones como 'var="valor"'
            RegExpresion = r'.*?Var.*?="(.*?)"'

            # Buscar todas las coincidencias usando findall
            VarFoundRaw = re.findall(RegExpresion, XML_Pdl)

            # Filtro para obeter solo las variables
            for var in (VarFoundRaw):
                try:
                    _ = int(var)
                except:
                    Variable = var.split(".")[0].replace(" ", "")
                    if len(Variable) > 1:
                        if not Variable in VarDefinidas:
                            XML_Pdl = XML_Pdl.replace(Variable, "ToDo")

        with open(Pdl, "w", encoding="UTF-16") as file:
            file.write(XML_Pdl)

    except:
        pass

    