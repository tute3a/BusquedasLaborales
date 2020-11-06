from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep  
import re
from datetime import datetime

driver = webdriver.Chrome("C:/Users/Administrator/chromedriver.exe")

total = []
listalinks = []
Hoy = datetime.today().strftime('%d-%m-%Y')

for pagina in range(500):         #Entra página por página
    if pagina > -1:             # Por si se corta en el medio
        #url = "https://www.zonajobs.com.ar/ofertas-de-empleo-argentina-pagina-" + str(pagina) + ".html?recientes=true"
        url = "https://www.zonajobs.com.ar/ofertas-de-empleo-publicacion-menor-a-15-dias-pagina-" + str(pagina) + ".html?recientes=true"
        driver.get(url)

        avisos = driver.find_element_by_class_name("aviso-no-sponsor")      #Lista de avisos
        links = avisos.find_elements_by_css_selector("a")

        for link in links:          #Busca el link de todos los avisos
            enlace = link.get_attribute('href')
            if enlace != None:                          # Por si no hay enlace dentro de los links que encuentra
                if enlace.find('/empleos/') > 0:        #Toma sólo los links de empleos
                    if not enlace in listalinks:        #Links que no se hayan abierto antes
                        print(enlace)
                        driver.execute_script("window.open('');")
                        driver.switch_to.window(driver.window_handles[1])
                        driver.get(enlace)              #En una nueva pestaña abre link por link
                        try:                            #Intenta los comandos conocidos (para evitar que falle)
                            try:                        #Comandos para Zonajobs
                                info = driver.find_element_by_class_name("aviso_specs").text
                                descripcion = driver.find_element_by_class_name("aviso_description").text
                                titulo = driver.find_element_by_class_name('aviso_title').text
                                empresa = driver.find_element_by_class_name('aviso_company').text

                                detalle = re.compile("\n(.*)").findall(info)
                                detalle = ((titulo, empresa, detalle[0], detalle[2].replace("Hoy", Hoy), detalle[4], detalle[6], detalle[8],
                                descripcion.replace("/n", "")))

                            except:                     #Comandos para Bumeran
                                info_1 = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/ul[1]').text
                                info_2 = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/ul[2]').text
                                descripcion = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[1]').text
                                empresa = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div[1]/div[1]/div/div[1]/div').text

                                info_1 = re.split("\n", info_1)
                                info_2 = re.split("\n", info_2)
                                empresa = re.split("\n", empresa)

                                detalle = ((empresa[0], empresa[1], info_1[1], info_1[0].replace("Hoy", Hoy), info_2[1], info_2[0],
                                info_2[2], descripcion))
                        except:                         #Salida si no encuentra ni ZonaJobs ni Bumeran
                            detalle = (('Error', 'Error', 'Error', 'Error', 'Error', 'Error', 'Error', 'Error'))
                            # Guardar el link
                            # Revisar si podemos guardar algo de info

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        el_link = ((enlace))
                        listalinks.append(el_link)      #Agrega el link abierto a la lista de links
                        total.append(detalle)           #Agrega la info a total

        print(pagina)
        df = pd.DataFrame(total, columns=['Trabajo', 'Empresa', 'Ubicación', 'Fecha', 'Salario', 'Jornada laboral', 'Área','Descripción'])
        print(df)       #Guarda una vez por página
        df.to_csv(r'C:\Users\Administrator\Desktop\Mati\Maestria UNLP\Economia de Género\ZonaJobsv3 - 22 octubre 2020 v2.csv', index=False, header=True)

df = pd.DataFrame(total,columns=['Trabajo','Empresa','Ubicación','Fecha','Salario','Jornada laboral','Área','Descripción'])
print(df)
driver.close()
df.to_csv (r'C:\Users\Administrator\Desktop\Mati\Maestria UNLP\Economia de Género\ZonaJobsv3 - 22 octubre 2020 v2.csv', index = False, header=True)
print("___________ FIN ___________")




