from bs4 import BeautifulSoup
from urllib.request import urlopen
import random

def imprimir():
    file = open("frases_inicio.txt","r")
    lista_datos = file.readlines()
    posicion = random.randint(0,25)
    print(lista_datos[posicion])

def manitas_a_la_obra(texto_limpio):
    f = open("frases_inicio.txt","w") #w: write
    for linea in texto_limpio:
        f.write(linea)

def fraccionar(texto):
    lineas = [linea for linea in texto.split('\n') if linea != '']
    lineas = lineas[87:111]                                                               #El numero se obtuvo de la posicion en el html
    texto_limpio = '\n'.join(lineas)
    manitas_a_la_obra(texto_limpio)

def main():
    global html

    url = "https://www.fundacionaquae.org/25-curiosidades-sobre-las-especies-marinas/"    #En caso de no funcionar se posee un respaldo
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    texto = soup.get_text()
    fraccionar(texto)
    imprimir()