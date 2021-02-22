import pandas as pd
import re
import numpy as np

encuesta = pd.read_excel (r'PATH\Encuesta Búsquedas Laborales.xlsx', sheet_name='Sheet', skiprows = 1)


genero = encuesta.iloc[:,9].astype(str)
for i in range(10,12):      # Son 3 columnas, la última (12) no está incluida
    genero = genero.astype(str) + encuesta.iloc[:,i].astype(str)
genero = genero.replace('nan', '', regex=True)
genero = genero.replace('Varón', '1', regex=True)
genero = genero.replace('Mujer', '0', regex=True)


edad = encuesta.iloc[:,12].astype(str)
for i in range(13,19):
    edad = edad.astype(str) + encuesta.iloc[:,i].astype(str)
edad = edad.replace('nan', '', regex=True)



educ = encuesta.iloc[:,19].astype(str)
for i in range(19,28):
    educ = educ.astype(str) + encuesta.iloc[:,i].astype(str)
educ = educ.replace('nan', '', regex=True)



control = encuesta.iloc[:,28].astype(str)
for i in range(29,30):
    control = control.astype(str) + encuesta.iloc[:,i].astype(str)
control = control.replace('nan', '', regex=True)



p1 = []
for i in range(0,len(encuesta)):
    valor = encuesta.iloc[i,30:45]
    try:
        indice = valor.first_valid_index()
        valor = valor[indice]
        indice = re.findall(r'[^.]+$', indice)[0]
        if str(indice) == 'Open-Ended Response':
            indice = 'M'
        elif int(indice) in [0,3,6,9,12]:
            indice = 'M'
        elif int(indice) in [1,4,7,10,13]:
            indice = 'F'
        elif int(indice) in [2,5,8,11,14]:
            indice = 'I'
    except:
        indice = '-'
        valor = '-'

    p1.append((valor,indice))

p1 = pd.DataFrame(p1,columns=['p1','p1_g'])
print(p1)



p2 = []
for i in range(0,len(encuesta)):
    rango = encuesta.iloc[i,45:75]
    try:
        indice = rango.first_valid_index()
        valor = rango[indice]
        lista_m = ["contador","biólogo","administrador","ingeniero","abogado"]
        lista_f = ["contadora", "bióloga", "administradora", "ingeniera", "abogada"]
        lista_i = ["contador/a", "biólogo/a", "administrador/a", "ingeniero/a", "abogado/a"]

        res = any(ele in valor for ele in lista_i)
        if res:
            p2_g = 'I'
        else:
            res = any(ele in valor for ele in lista_f)
            if res:
                p2_g = 'F'
            else:
                res = any(ele in valor for ele in lista_m)
                if res:
                    p2_g = 'M'

        indice = re.findall(r'[^.]+$', indice)[0]
        if str(indice) == 'Question Viewed':
            indice = 0
        indice = int(indice) + 15
        valor = "Open-Ended Response." + str(indice)
        valor = rango[str(valor)]


    except:
        valor = '-'
        p2_g = '-'

    p2.append((valor, p2_g))

p2 = pd.DataFrame(p2,columns=['p2','p2_g'])



p3 = encuesta.iloc[:,75].astype(str)
p3 = p3.replace('nan', '-', regex=True)


p4 = encuesta.iloc[:,77].astype(str)
p4 = p4.replace('nan', '-', regex=True)


p4_g = encuesta.iloc[:,76].str.contains('mujer')
p4_g = p4_g.replace(True, 'F', regex=True)
p4_g = p4_g.replace(False, 'M', regex=True)
p4_g = p4_g.replace(np.nan, '-', regex=True)


id = genero + p1['p1_g'] + p2['p2_g'] + p4_g
result = pd.concat([id,genero, edad, educ, control,p1['p1'],p1['p1_g'],p2['p2'],p2['p2_g'],p3, p4, p4_g], axis=1)
result.rename(columns={result.columns[0]:'ID',
                       result.columns[1]:'Género',
                       result.columns[2]:'Edad',
                       result.columns[3]:'Educación',
                       result.columns[4]:'Control',
                       result.columns[5]:'Pregunta 1',
                       result.columns[6]:'Pregunta 1 género',
                       result.columns[7]:'Pregunta 2',
                       result.columns[8]:'Pregunta 2 género',
                       result.columns[9]:'Pregunta 3',
                       result.columns[10]:'Pregunta 4',
                       result.columns[11]:'Pregunta 4 género'}, inplace=True)
print(result)

result.to_csv (r'C:\Users\Administrator\Desktop\Mati\Maestria UNLP\Economia de Género\ResultadosEncuestaAgrupados.csv', index = False, header=True, encoding='utf_8_sig')


