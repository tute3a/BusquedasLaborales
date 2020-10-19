import pandas as pd
from Genero_funciones import tranf_titulo, busqueda_palabras, define_genero

# Archivo de profesiones y palabras con las que compara
df_prof = pd.read_excel (r'C:\Users\Administrator\Desktop\profesiones.xlsx')

# Archivo donde clasifica el género
df = pd.read_excel (r'C:\Users\Administrator\Desktop\ZonaJobs testeo.xlsx', sheet_name='ZonaJobs')
titulos = df.Trabajo

final = []

for titulo in titulos:
    titulo = tranf_titulo(titulo)
    genero = busqueda_palabras(titulo,df_prof)
    genero = define_genero(genero)
    final.append((titulo, genero))


df = pd.DataFrame(final,columns=['Titulo','Genero'])
print(df)

# Guarda los títulos y el género
df.to_csv (r'C:\Users\ResultadoGenero.csv', index = False, header=True)



