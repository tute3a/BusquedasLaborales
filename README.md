# ¿Qué hace cada archivo?
El archivo Busquedas hace el scraping de ZonaJobs y Bumeran (BusquedasLaborales.py es el archivo original para eso pero quedó viejo por la actualización de la página de Bumeran).

El archivo Genero.py clasifica el género, llamando funciones que están en el archivo Genero_funciones.py





## Lista de librerías necesarias
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import re
from datetime import datetime
import spacy
from googletrans import Translator
