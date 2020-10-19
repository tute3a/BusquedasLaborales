## BusquedasLaborales
El archivo BusquedasLaborales.py hace el scraping de ZonaJobs y Bumeran.

El archivo Genero.py clasifica el género, llamando funciones que están en el archivo Genero_funciones.py





# Lista de ibrerías necesarias
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import re
from datetime import datetime
import spacy
from googletrans import Translator
