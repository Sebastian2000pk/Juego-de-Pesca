import pygame, sys

from random import randrange
pygame.init()


#---------------------------------------variables de configuracion----------------------------
color = 255, 255, 255 # Color de fondo base
c = 25,25,25
size = (720, 480) # Tamaño de la ventana
precionado = False # Variable que registra si esta o no presionado el boton de jugar
reloj = pygame.time.Clock()
pantalla = 1
fps = 30 # Fps del juego



#---------------------------------------variables-----------------------------------------------
reg_peces = [] # Almacena las instancias de los peces


#---------------------------------------Cargar imagenes----------------------------------------
img_boton_jugar = pygame.image.load("images/boton_jugar.png") # Boton jugar
img_boton_jugar = pygame.transform.scale(img_boton_jugar, (285, 125))
img_fondo_mar = pygame.image.load("images/fondo mar.jpg") # Fondo del mar
img_fondo_mar = pygame.transform.scale(img_fondo_mar, (720, 480))
imagenes_peces = [pygame.image.load("images/pez azul.png"), # Carga imagen de pez azul
pygame.image.load("images/pez morado.png"), # Carga imagen de pez morado
pygame.image.load("images/pez rojo.png"),  # Carga imagen de pez rojo
pygame.image.load("images/pez verde.png")] # Carga imagen de pez verde
imagenes_peces[0] = pygame.transform.scale(imagenes_peces[0], (59, 53)) # Escalar la imagen pez azul
imagenes_peces[1] = pygame.transform.scale(imagenes_peces[1], (67, 51)) # Escalar la imagen pez morado
anzuelo_vacio = pygame.image.load("images/canna.png") # Carga imagen de anzuelo vacio
anzuelo_carnada = pygame.image.load("images/canna_carnada.png") # Carga imagen de anzuelo con carnada


screen = pygame.display.set_mode(size) # Iniciar la ventana
pygame.display.set_caption("Juego de pesca") # Cambiar nombre de la ventana


#---Funciones-------------------------------------------------------------------------------------
def Crear_boton_jugar(x, y, pre): # Funcion que crear el boton jugar
    screen.blit(img_boton_jugar, (x, y)) # Mostrar el boton jugar
    ancho = img_boton_jugar.get_width() # Ancho de la imagen
    alto = img_boton_jugar.get_height() # Alto de la imagen
    pos1 = x + 30, y + 30 # Posicion 1 del area de colision
    pos2 = x + ancho - 30, y + alto - 30 # Posicion 2 del area de colision
    mouse_pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pos1[0] < mouse_pos[0] < pos2[0] and pos1[1] < mouse_pos[1] < pos2[1] and pre == False: # Verifica si se esta precionando el mouse y si esta desntro del area del boton
        return True
    else:
        return precionado

def Crear_pez(t): # Funcion para crear los peces
    p = Peces(t, len(reg_peces)) # crea la instancia del objeto pez
    reg_peces.append(p) # Añade la entidad al registro de peces
    

xf = 1
#---Clases-------------------------------------------------------------------------------------------
class Anzuelo:
    def __init__(self):
        global anzuelo_carnada
        global anzuelo_vacio
        self.xAnz = 340 # posicion en X del anzuelo
        self.Yanz = 200 

    def mostrar(self): # Funcion para mostrar la imagen del anzuelo
        mouse_pos = pygame.mouse.get_pos() # recupera posicion del mouse
        if mouse_pos[1] > 65 and mouse_pos[1] < 460: # Limite Y del anzuelo
            self.Yanz = mouse_pos[1] - 25
        
        screen.blit(anzuelo_carnada, [self.xAnz, self.Yanz]) # Muestra puntero --> anzuelo
        pygame.draw.line(screen, (0, 0, 0), [360, 55], [360, self.Yanz + 15], 1)


class Peces:
    def __init__(self, t, posA):
        global imagenes_peces
        self.posArray = posA
        self.x = 0 # Posicion X inicial
        self.tipo = t # Tipo de pez, sirve para usarlo dentro de la variable que almacena las imagenes de los peces
        self.velocidad = 1 # Velocidad de desplazamiento
        self.y = randrange(100, 440) # Definir pocision aleatoria del eje Y
        self.pos_x = randrange(0,2)
        if self.pos_x == 1:
            self.x = 700
            self.velocidad = -1
        
    def mos(self): # Metodo para mostrar la imagen
        img = imagenes_peces[self.tipo] # Guarda la imagen del pes
        if self.velocidad > 0:
            img = pygame.transform.flip(img, True, False) # Si avanza a la derecha, le da la vuelta a la imagen
        screen.blit(img, (self.x, self.y)) # Mostrar imagen del pez
        if self.x < -55 or self.x > 720: # Verifica que la instancia se encuentre dentro de los limites
            reg_peces.remove(self) # Elimina la instancia del registro

    def movimiento(self): # Metodo para mover la imagen
        self.x += 2*self.velocidad # Aumenta o reduce la pocision en X dependiento de la velocidad

    def Eliminar(self): # Metodo para eliminar la entidad si sobrepasa los limites
        reg_peces.remove(self) # Elimina la instancia del registro

Crear_pez(0)
Crear_pez(1)
Crear_pez(0)

#--------Ciclo de actuializacion de pantalla de inicio-------------------------------------------------
while pantalla == 1:
    reloj.tick(fps) # Velocidad a la que corre el juego

    for event in pygame.event.get(): # Detecta los eventos
        if event.type == pygame.QUIT: sys.exit() # Si el evento fue presionar la X, se cierra el programa

    screen.fill(color) # Rellena el fondo
    #--Las imagenes van despues de esta linea

    precionado = Crear_boton_jugar(220, 150, precionado)
    if precionado:
        pantalla = 2 # Cambia de pantalla

    #--Las imagenes van antes de esta linea
    pygame.display.update() # Actualiza la imagen de la ventana

anz = Anzuelo()
#-------- Ciclo de actualizacion de pantalla de juego----------------------------------------------------
while pantalla == 2:
    reloj.tick(fps) # Velocidad a la que corre el juego
    pygame.mouse.set_visible(0) # Desaparece el puntero

    for event in pygame.event.get(): # Detecta los eventos
        if event.type == pygame.QUIT: sys.exit() # Si el evento fue presionar la X, se cierra el programa

    screen.fill(color) # Rellena el fondo
    #--Las imagenes van despues de esta linea------------------------------


    screen.blit(img_fondo_mar, (0, 0)) # Mostrar fondo "mar"

    ind_registro = len(reg_peces) - 1 # Indice del registro
    while ind_registro != -1: # Actualiza los metodos de cada instancia "peces"
        reg_peces[ind_registro].movimiento() # Llama a la funcion para mover el pez
        reg_peces[ind_registro].mos() # llama a la funcion para visualizar el pez
        ind_registro -= 1 # Disminuye en uno el numero de indices
    
    anz.mostrar() # muestra el anzuelo en la pantalla


    #--Las imagenes van antes de esta linea---------------------------------
    pygame.display.update() # Actualiza la imagen de la ventana
