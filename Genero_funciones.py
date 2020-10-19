import pandas as pd
import re
import spacy
from googletrans import Translator #Para detectar el idioma


nlp = spacy.load('es')
translator = Translator()

def detecta_idioma(texto):
    """
    DEVUELVE EL IDIOMA DEL TÍTULO ('es' para español, 'en' para inglés, etc.).
    """

        # Para evitar que reconozca mal palabras de pocos caracteres
    if len(texto) >= 5:
        idioma = translator.detect(texto)

            # Si tiene más del 90% de confianza en el idioma identificado se lo asigna
        if idioma.confidence >= 0.9:
            idioma = idioma.lang

            # Si tiene menos le asigna español para que busque palabras
        else:
            idioma = 'es'
    else:
        idioma = 'es'

    return idioma




def tranf_titulo(titulo_original):
    """
    NORMALIZA EL TITULO PARA EVITAR ERRORES DE RECONOCIMIENTO
    """

    # Pasamos todo a minúsculas
    nuevo_titulo = titulo_original.lower()

    # Hay casos donde escriben "abogado-a", con esto unificamos a "abogado/a"
    nuevo_titulo = re.sub(r'[-]',r'/',nuevo_titulo)

    # Sacamos el resto de los simbolos más comunes
    nuevo_titulo = re.sub(r'[?|!|.|:|(|)|*|,|+]',r'',nuevo_titulo)

    # Saca espacios cuando es inclusivo. Ejemplo: "abogado / a"

        #Cuando después de la última parte hay espacio
    nuevo_titulo = re.sub(r'o / a ',r'o/a ',nuevo_titulo)
    nuevo_titulo = re.sub(r'os / as ',r'os/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'es / as ',r'es/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'a / o ',r'a/o ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as / os ',r'as/os ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as / es ',r'as/es ',nuevo_titulo)

    nuevo_titulo = re.sub(r'o/ a ',r'o/a ',nuevo_titulo)
    nuevo_titulo = re.sub(r'os/ as ',r'os/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'es/ as ',r'es/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'a/ o ',r'a/o ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as/ os ',r'as/os ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as/ es ',r'as/es ',nuevo_titulo)

    nuevo_titulo = re.sub(r'o /a ',r'o/a ',nuevo_titulo)
    nuevo_titulo = re.sub(r'os /as ',r'os/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'es /as ',r'es/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'a /o ',r'a/o ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as /os ',r'as/os ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as /es ',r'as/es ',nuevo_titulo)

        #Cuando después de la última parte termina la oración
    nuevo_titulo = re.sub(r'o / a$',r'o/a ',nuevo_titulo)
    nuevo_titulo = re.sub(r'os / as$',r'os/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'es / as$',r'es/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'a / o$',r'a/o ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as / os$',r'as/os ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as / es$',r'as/es ',nuevo_titulo)

    nuevo_titulo = re.sub(r'o/ a$',r'o/a ',nuevo_titulo)
    nuevo_titulo = re.sub(r'os/ as$',r'os/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'es/ as$',r'es/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'a/ o$',r'a/o ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as/ os$',r'as/os ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as/ es$',r'as/es ',nuevo_titulo)

    nuevo_titulo = re.sub(r'o /a$',r'o/a ',nuevo_titulo)
    nuevo_titulo = re.sub(r'os /as$',r'os/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'es /as$',r'es/as ',nuevo_titulo)
    nuevo_titulo = re.sub(r'a /o$',r'a/o ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as /os$',r'as/os ',nuevo_titulo)
    nuevo_titulo = re.sub(r'as /es$',r'as/es ',nuevo_titulo)

        # Casos especiales en donde usan sigular y plural (ej. tecnico/as)
    nuevo_titulo = re.sub(r"o/as ", "o/a ", nuevo_titulo)
    nuevo_titulo = re.sub(r"o/as$", "o/a", nuevo_titulo)
    nuevo_titulo = re.sub(r"a/os ", "a/o ", nuevo_titulo)
    nuevo_titulo = re.sub(r"a/os$", "a/os", nuevo_titulo)

        # Cuando la palabra tiene caracteres unidos
            #Cuando está al final de la palabra, lo separamos con un espacio
    nuevo_titulo = re.sub(r'/ ',r' / ',nuevo_titulo)

            #Cuando está al principio de la palabra, lo separamos con un espacio
    nuevo_titulo = re.sub(r' /',r' / ',nuevo_titulo)

            #Cuando está al final del texto
    nuevo_titulo = re.sub(r'/$',r'',nuevo_titulo)

            #Cuando está al principio del texto
    nuevo_titulo = re.sub(r'^/',r'',nuevo_titulo)


    # Sacamos expresiones comunes

        # Sacamos del "para" en adelante para evitar errores como con "quimica" en:
                # "Soldador para importante empresa Quimica de zona Sur"
                # Sería un título M, pero lo trae como F por decir "quimica"
    nuevo_titulo = re.sub(r" para .*", "", nuevo_titulo)

        # Sacamos todo lo que sigue a lo relacionado con industria (industria, industrial, etc)
                #  Suele aparecer al final. Si está al principio sería un problema.
    nuevo_titulo = re.sub(r" industria .*", "", nuevo_titulo)

        # Sacamos "estudiante de" + 1 palabra para que no confunda el género
    nuevo_titulo = re.sub(r"estudiante de (\w+)", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"estudiantes de (\w+)", " ", nuevo_titulo)

        # Sacamos "ayudante de" + 1 palabra para que no confunda el género, y le asignamos genérico
    nuevo_titulo = re.sub(r"ayudante de (\w+)", " generico ", nuevo_titulo)
    nuevo_titulo = re.sub(r"ayudantes de (\w+)", " generico ", nuevo_titulo)

        # Sacamos "asistente de" + 1 palabra para que no confunda el género, y le asignamos genérico
    nuevo_titulo = re.sub(r"asistente de (\w+)", " generico ", nuevo_titulo)
    nuevo_titulo = re.sub(r"asistente de (\w+)", " generico ", nuevo_titulo)

        # Sacamos "soporte técnico" para que no confunda técnico con masculino
    nuevo_titulo = re.sub(r" soporte tecnico ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" soporte tecnico$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^soporte tecnico ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^soporte tecnico$", " ", nuevo_titulo)

        # Sacamos "servicio técnico" para que no confunda técnico con masculino
    nuevo_titulo = re.sub(r" servicio tecnico ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" servicio tecnico$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^servicio tecnico ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^servicio tecnico$", " ", nuevo_titulo)

        # Sacamos "compras técnicas" para que no confunda técnicas con femenino
    nuevo_titulo = re.sub(r" compras tecnicas ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" compras tecnicas$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^compras tecnicas ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^compras tecnicas$", " ", nuevo_titulo)

        # Sacamos "area técnica" para que no confunda técnica con femenino
    nuevo_titulo = re.sub(r" area tecnica ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" area tecnica$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^area tecnica ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^area tecnica$", " ", nuevo_titulo)

        # Sacamos "seguridad informática" para que no confunda informática con femenino
    nuevo_titulo = re.sub(r" seguridad informatica ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" seguridad informatica$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^seguridad informatica ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^seguridad informatica$", " ", nuevo_titulo)

        # Sacamos "riesgo informático" para que no confunda informático con masculino
    nuevo_titulo = re.sub(r" riesgo informatico ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" riesgo informatico$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^riesgo informatico ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^riesgo informatico$", " ", nuevo_titulo)

        # Sacamos "pago a proveedores" para que no confunda proveedores con masculino
    nuevo_titulo = re.sub(r" pago a proveedores ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" pago a proveedores$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^pago a proveedores ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^pago a proveedores$", " ", nuevo_titulo)

        # Sacamos "uso veterinario" para que no confunda veterinario con masculino
    nuevo_titulo = re.sub(r" uso veterinario ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" uso veterinario$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^uso veterinario ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^uso veterinario$", " ", nuevo_titulo)

        # Sacamos "material medico" para que no confunda médico con masculino
    nuevo_titulo = re.sub(r" material medico ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" material medico$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^material medico ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^material medico$", " ", nuevo_titulo)

        # Sacamos "servicio medico" para que no confunda médico con masculino
    nuevo_titulo = re.sub(r" servicio medico ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" servicio medico$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^servicio medico ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^servicio medico$", " ", nuevo_titulo)

        # Sacamos "puesto administativo" para que no confunda administrativo con masculino
    nuevo_titulo = re.sub(r" puesto administrativo ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" puesto administrativo$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^puesto administrativo ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^puesto administrativo$", " ", nuevo_titulo)

        # Sacamos "personal administativo" para que no confunda administrativo con masculino
    nuevo_titulo = re.sub(r" personal administrativo ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" personal administrativo$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^personal administrativo ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^personal administrativo$", " ", nuevo_titulo)

        # Sacamos "perfil administativo" para que no confunda administativo con masculino
    nuevo_titulo = re.sub(r" perfil administativo ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" perfil administativo$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^perfil administativo ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^perfil administativo$", " ", nuevo_titulo)

        # Sacamos "tareas administativas" para que no confunda administativas con femenino
    nuevo_titulo = re.sub(r" tareas administativas ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" tareas administativas$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^tareas administativas ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^tareas administativas$", " ", nuevo_titulo)

        # Sacamos "area administrativa" para que no confunda administrativa con femenino
    nuevo_titulo = re.sub(r" area administrativa ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" area administrativa$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^area administrativa ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^area administrativa$", " ", nuevo_titulo)

        # Sacamos "perfil financiero" para que no confunda financiero con masculino
    nuevo_titulo = re.sub(r" perfil financiero ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" perfil financiero$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^perfil financiero ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^perfil financiero$", " ", nuevo_titulo)

        # Sacamos "productos financieros" para que no confunda financieros con masculino
    nuevo_titulo = re.sub(r" productos financieros ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" productos financieros$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^productos financieros ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^productos financieros$", " ", nuevo_titulo)

        # Sacamos "entidades financieras" para que no confunda financieras con femenino
    nuevo_titulo = re.sub(r" entidades financieras ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" entidades financieras$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^entidades financieras ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^entidades financieras$", " ", nuevo_titulo)

    # Sacamos "entidad financiera" para que no confunda financiera con femenino
    nuevo_titulo = re.sub(r" entidad financiera ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r" entidad financiera$", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^entidad financiera ", " ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^entidad financiera$", " ", nuevo_titulo)

    # Cambiamos sexo femenino para que lo detecte como femenino
    nuevo_titulo = re.sub(r" sexo femenino ", " femenino ", nuevo_titulo)
    nuevo_titulo = re.sub(r" sexo femenino$", " femenino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^sexo femenino ", " femenino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^sexo femenino$", " femenino ", nuevo_titulo)

    # Cambiamos sexo masculino para que lo detecte como masculino
    nuevo_titulo = re.sub(r" sexo masculino ", " masculino ", nuevo_titulo)
    nuevo_titulo = re.sub(r" sexo masculino$", " masculino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^sexo masculino ", " masculino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^sexo masculino$", " masculino ", nuevo_titulo)

    # Cambiamos personal femenino para que lo detecte como femenino
    nuevo_titulo = re.sub(r" personal femenino ", " femenino ", nuevo_titulo)
    nuevo_titulo = re.sub(r" personal femenino$", " femenino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^personal femenino ", " femenino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^personal femenino$", " femenino ", nuevo_titulo)

    # Cambiamos personal masculino para que lo detecte como masculino
    nuevo_titulo = re.sub(r" personal masculino ", " masculino ", nuevo_titulo)
    nuevo_titulo = re.sub(r" personal masculino$", " masculino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^personal masculino ", " masculino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^personal masculino$", " masculino ", nuevo_titulo)

    # Cambiamos agente inmobiliaria para que lo detecte como femenino
    nuevo_titulo = re.sub(r" agente inmobiliaria ", " femenino ", nuevo_titulo)
    nuevo_titulo = re.sub(r" agente inmobiliaria$", " femenino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^agente inmobiliaria ", " femenino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^agente inmobiliaria$", " femenino ", nuevo_titulo)

    # Cambiamos agente inmobiliario para que lo detecte como masculino
    nuevo_titulo = re.sub(r" agente inmobiliario ", " masculino ", nuevo_titulo)
    nuevo_titulo = re.sub(r" agente inmobiliario$", " masculino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^agente inmobiliario ", " masculino ", nuevo_titulo)
    nuevo_titulo = re.sub(r"^agente inmobiliario$", " masculino ", nuevo_titulo)

    
    return nuevo_titulo





def define_genero (matriz):
    """
    DEFINE UN VALOR ÚNICO PARA EL GÉNERO
    """

    genero_nueva = []

    # Si en todo el título no encontró le asigna genérico
    if not len(matriz):
        genero_nueva.append("generico")

    # Si encontró algo se fija a qué categoría asignarlo
    # Por cada valor que encuentra suma 1 a las variables de abajo
    else:
        m = 0
        f = 0
        i = 0
        g = 0
        s = 0
        for sexo in matriz:
            if sexo == 'femenino':
                f = f + 1
            elif sexo == 'inclusivo':
                i = i + 1
            elif sexo == 'masculino':
                m = m + 1
            elif sexo == 'generico':
                g = g + 1
            elif sexo == 'masculino_spacy':
                s = s + 1
            elif sexo == 'femenino_spacy':
                s = s + 1


        if f > 0 and i == 0 and m == 0 and g == 0:
            genero_nueva.append('femenino')
        elif f > 0 and i == 0 and m == 0 and g > 0:
            genero_nueva.append('femenino')
        elif f == 0 and i == 0 and m > 0 and g == 0:
            genero_nueva.append('masculino')
        elif f == 0 and i == 0 and m > 0 and g > 0:
            genero_nueva.append('masculino')
        elif i > 0:
            genero_nueva.append('inclusivo')
        elif f == 0 and i == 0 and m == 0 and g > 0 and s == 0:
            genero_nueva.append('generico')
        elif s > 0:
            genero_nueva.append('REVISAR A MANO')
        elif f != 0 and m != 0:
            genero_nueva.append('REVISAR A MANO')


    # Dejamos sólo las palabras, sin [] ni '
    genero_nueva = str(genero_nueva).replace("['", '').replace("']", '')


    return genero_nueva





def busqueda_spacy(texto):
    """"
    BUSCA EN LOS TÍTULOS LOS ADJETIVOS RELACIONADOS AL SUSTANTIVO PRINCIPAL Y LES ASIGNA EL GÉNERO.
    SIRVE PARA ENCONTRAR LAS QUE TENEMOS QUE CLASIFICAR A MANO.
    """

    doc = nlp(texto)
    sust_ppal = ''
    detalles = ''

    for token in doc:
        # token.text muestra la palabra
        # token.pos_ muestra el tipo de palabra: verbo, sustantivo, adjetivo, etc.
        # token.dep_ muestra la dependencia sintáctica, es decir la relación con otras palabras
        # token.head.pos_ muestra el tipo de palabra (verbo, sust, etc.) a la que está relacionada
        # token.head.text muestra la palabra a la que está relacionada
        # token.tag_ muestra detalles de la palabra: género, número, etc.
        # Para ver más cosas: https://spacy.io/usage/linguistic-features

            # Si es el sustantivo principal lo guarda
        if token.pos_ == "NOUN" and token.dep_ == "ROOT":
            sust_ppal = token.text


            # Si es un adjetivo que depende del sustantivo principal analiza el género
        if token.pos_ == "ADJ" and token.head.text == sust_ppal:
            detalles = token.tag_

            if "Masc" in detalles:
                detalles = "masculino_spacy"
            elif "Fem" in detalles:
                detalles = "femenino_spacy"
            else:
                detalles = "generico"

    return detalles





def busqueda_palabras(title, database):
    """"
    BUSCA LOS TITULOS EN LA LISTA Y LE ASIGNA UN GENERO A CADA PALABRA
    """
    # Database es la lista de palabras contra la que compara

    gender = []

    # Mira el idioma del título
    idioma = detecta_idioma(title)

        # Si es inglés le asigna genérico
    if idioma == 'en':
        gender.append('generico')


        # Si no es inglés analiza palabra a palabra
    else:
        palabras = title.split()

        for palabra in palabras:
            busqueda = database[database['profesion'] == palabra]

            # Si encontró algo en la lista lo guarda
            if (not busqueda.empty):
                # Guarda el valor de la columna de género de la base de búsqueda
                gender.append(busqueda.genero.values[0])

                # Si no encontró nada revisa si hay palabras unidas por algún caracter especial
                # Ejemplo "sistemas/informatica/programacion"
            if (busqueda.empty):
                doc = nlp(palabra)
                for token in doc:
                    palabra_unida = token.text
                    busqueda = database[database['profesion'] == palabra_unida]

                    # Si encontró algo en las palabras separadas lo guarda
                    if (not busqueda.empty):
                        # Guarda el valor de la columna de género de la base de búsqueda
                        gender.append(busqueda.genero.values[0])


        genero = define_genero(gender)

        # Si no encontró en el listado, busca las palabras con spacy
        if len(gender) == 0:
            resultado_spacy = busqueda_spacy(title)
                # Si encontró algo usando spacy que lo agregue
            if not resultado_spacy == '':
                gender.append(resultado_spacy)
        elif genero == 'generico':
            resultado_spacy = busqueda_spacy(title)

            if not resultado_spacy == '':
                gender.append(resultado_spacy)

    return gender


