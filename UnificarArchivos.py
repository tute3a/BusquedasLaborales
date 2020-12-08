"""
UNIFICA TODOS LOS ARCHIVOS GUARDADOS DENTRO DE UNO SOLO.
HAY QUE CAMBIAR PATH POR EL DIRECTORIO DONDE TENEMOS TODOS LOS ARCHIVOS.
"""

import os
import pandas as pd
import re

# Traemos todos los archivos de un directorio
os.chdir(r"PATH" )
path = os.getcwd()
files = os.listdir(path)
print(files)

# Definimos los archivos XLS
files_xlsx = [f for f in files if f[-4:] == 'xlsx']
print(files_xlsx)

# Definimos los archivos CSV
files_csv = [f for f in files if f[-3:] == 'csv']
print(files_csv)

# Unimos los archivos
df = pd.DataFrame()

# Para cambiar la fecha usamos las variables inicio y fin
inicio = 13

for file in files_csv:
    data = pd.read_csv(file, encoding = 'utf-8')
    data.columns = ['Trabajo', 'Empresa', 'Ubicación', 'Fecha', 'Salario', 'Jornada laboral', 'Área', 'Descripción']

    # Busca la fecha de ayer y lo cambia restadole un dia a la de hoy
    fin = len(file) - 4
    texto_fecha = file[inicio:fin]
    fecha = int(texto_fecha[0:texto_fecha.find('-')])-1
    fecha = str(fecha) + texto_fecha[texto_fecha.find('-'):]
    data['Fecha'] = data['Fecha'].replace('Ayer', str(fecha), regex=True)

    df = df.append(data)
    print("El archivo ahora tiene " + str(len(df)) + " lineas, porque se agregó un archivo de " + str(
        len(data)) + " lineas")


for file in files_xlsx:
    data = pd.read_excel(file, encoding = 'utf-8')
    data.columns = ['Trabajo', 'Empresa', 'Ubicación', 'Fecha', 'Salario', 'Jornada laboral', 'Área','Descripción']

    # Busca la fecha de ayer y lo cambia restadole un dia a la de hoy
    fin = len(file) - 5
    texto_fecha = file[inicio:fin]
    fecha = int(texto_fecha[0:texto_fecha.find('-')])-1
    fecha = str(fecha) + texto_fecha[texto_fecha.find('-'):]
    data['Fecha'] = data['Fecha'].replace('Ayer', str(fecha), regex=True)

    df = df.append(data)
    print("El archivo ahora tiene " + str(len(df)) + " lineas, porque se agregó un archivo de " + str(
        len(data)) + " lineas")

#FALTA QUE CAMBIE EL DIA Y PONGA CUAL ES EL DIA DE AYER

# Cambiamos los caracteres raros
df = df.replace('Á','A', regex=True)
df = df.replace('É','E', regex=True)
df = df.replace('Í','I', regex=True)
df = df.replace('Ó','O', regex=True)
df = df.replace('Ú','U', regex=True)
df = df.replace('á','a', regex=True)
df = df.replace('é','e', regex=True)
df = df.replace('í','i', regex=True)
df = df.replace('ó','o', regex=True)
df = df.replace('ú','u', regex=True)


df = df.replace('Ã','A', regex=True)
df = df.replace('Ã ','A', regex=True)
df = df.replace('Ã¡','a', regex=True)
df = df.replace('ÃƒÂ ','a', regex=True)

df = df.replace('Ã‰','E', regex=True)
df = df.replace('Ãˆ','E', regex=True)
df = df.replace('Ã©','e', regex=True)
df = df.replace('Ã¨','e', regex=True)

df = df.replace('Ã','I', regex=True)
df = df.replace('Ã­','i', regex=True)
df = df.replace('Ã¬','i', regex=True)

df = df.replace('Ã“','O', regex=True)
df = df.replace('Ãƒâ€™','O', regex=True)
df = df.replace('Ã³','o', regex=True)
df = df.replace('Ã²','o', regex=True)

df = df.replace('Ãš','U', regex=True)
df = df.replace('Ãº','u', regex=True)
df = df.replace('Ã¹','u', regex=True)
df = df.replace('Ã¼','u', regex=True)

df = df.replace('Ã‘','Ñ', regex=True)
df = df.replace('Ã±','ñ', regex=True)

print(df)
df.to_csv(r'Zonajobs VersionUnificada.csv',
          index=False)
