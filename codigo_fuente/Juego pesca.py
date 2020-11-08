import pygame, sys

from random import randrange
pygame.init()



#---------------------------------------variables-----------------------------------------------
reg_peces = [] # Almacena las instancias de los peces
puntos = 0 # numero de puntos
estado_anzuelo = 1 # estados del anzuelo (0:sin carnada, 1:con carnada, 2:con pez)
start_time_ticks = pygame.time.get_ticks() # tiempo de inicio del contador para la generacion de peces
last_time_ticks = start_time_ticks # tiempo requerido inicial para generar peces es de 0 seg



#---Funciones-------------------------------------------------------------------------------------
def Reproducir_musica(ruta, vol, num):
    pygame.mixer.music.load(ruta) # carga la musica de fondo
    pygame.mixer.music.set_volume(vol) # cambiamos el volumen
    pygame.mixer.music.play(num) # reproduce la cancion

def Generar_peces(frecuencia, imagenes_peces): # funcion para generar peces
    global last_time_ticks, start_time_ticks
    last_time_ticks = pygame.time.get_ticks() # se le asigna al ultimo ticks, los ticks actuales
    if last_time_ticks >= start_time_ticks + (frecuencia*1000): # verifica si el tiempo actual es mayor al tiempo inicial mas la frecuencia
        start_time_ticks = pygame.time.get_ticks() # para que se inicie de nuevo el contador
        Crear_pez(randrange(0,2), imagenes_peces) # crea una instancia de los peces

def muestra_texto(texto, dimensiones, x, y, screen, fuente):
    tipo_letra = pygame.font.Font(fuente, dimensiones) # defin el tipo de letra del texto
    superficie = tipo_letra.render(texto, True, (0, 0, 0)) # crea la imagen del texto
    rectangulo = superficie.get_rect() # recupera el rectangulo de la imagen del texto
    rectangulo.centerx = x 
    rectangulo.centery = y
    screen.blit(superficie, rectangulo) # muestra la imagen del texto
    
def Crear_boton_jugar(x, y, pre, screen, img_boton_jugar, event): # Funcion que crear el boton jugar
    screen.blit(img_boton_jugar, (x, y)) # Mostrar el boton jugar
    ancho = img_boton_jugar.get_width() # Ancho de la imagen
    alto = img_boton_jugar.get_height() # Alto de la imagen
    pos1 = x + 30, y + 30 # Posicion 1 del area de colision
    pos2 = x + ancho - 30, y + alto - 30 # Posicion 2 del area de colision
    mouse_pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pos1[0] < mouse_pos[0] < pos2[0] and pos1[1] < mouse_pos[1] < pos2[1] and pre == False: # Verifica si se esta precionando el mouse y si esta desntro del area del boton
        return True
    else:
        return pre

def Crear_pez(t, imagenes_peces): # Funcion para crear los peces
    global reg_peces
    p = Peces(t, len(reg_peces), imagenes_peces) # crea la instancia del objeto pez
    reg_peces.append(p) # Añade la entidad al registro de peces
    

#---Clases-------------------------------------------------------------------------------------------
class Anzuelo:
    def __init__(self, rectangulo_anzuelo, img_anzuelo):
        self.conCarnada = 1 # para saber cuando tiene o no carnada
        self.imagenSi = img_anzuelo[0] # se define como imagen iniciar, el anzuelo con carnada
        self.xAnz = 340 # posicion en X del anzuelo
        self.Yanz = 200  # posicion Y del anzuelo
        rectangulo_anzuelo.left = self.xAnz # le da posicion en X al rectangulo
        rectangulo_anzuelo.top = self.Yanz # le da posicion en Y al rectangulo

    def mostrar(self, rectangulo_anzuelo, img_anzuelo, screen, estado_anzuelo): # Funcion para mostrar la imagen del anzuelo
        self.conCarnada = estado_anzuelo
        mouse_pos = pygame.mouse.get_pos() # recupera posicion del mouse
        if mouse_pos[1] > 65 and mouse_pos[1] < 460: # Limite Y del anzuelo
            rectangulo_anzuelo.top = mouse_pos[1] - 25  # Actualiza la posicion del anzuelo
        if self.conCarnada == 1: # verifica si tiene carnada o no
            self.imagenSi = img_anzuelo[1] # como tiene carnada, muestra la imagen con carnada
        else:
            self.imagenSi = img_anzuelo[0] # como no tiene carnada, muestra la imagen sin carnada
        screen.blit(self.imagenSi, rectangulo_anzuelo) # Muestra puntero --> anzuelo
        pygame.draw.line(screen, (0, 0, 0), [360, 55], [360, rectangulo_anzuelo.top + 15], 1) # dibujar la linea del anzuelo

    def Actualizar_estado(self, x): # funcion para cambiar el estado del anzuelo (con carnada, sin carnada)
        self.conCarnada = x



class Peces:
    def __init__(self, t, posA, imagenes_peces):
        self.muerto = False # define si debe borrarse o no la entidad
        self.atrapado = False
        self.posArray = posA # recupera su pocicion inicial en el array
        self.x = -55 # Posicion X inicial
        self.tipo = t # Tipo de pez, sirve para usarlo dentro de la variable que almacena las imagenes de los peces
        self.velocidad = 1 # Velocidad de desplazamiento
        self.y = randrange(100, 440) # Definir pocision aleatoria del eje Y
        self.pos_x = randrange(0,2)
        if self.pos_x == 1:
            self.x = 700
            self.velocidad = -1 # Cambia la direccion en la que se mueve el pez
        self.rectangulo = imagenes_peces[self.tipo].get_rect() # Guarda el rectangulo de pez
        self.rectangulo.left = self.x # darle posicion al rectangulo en X
        self.rectangulo.top = self.y
        
    def mos(self, imagenes_peces, screen, rectangulo_anzuelo): # Metodo para mostrar la imagen
        global estado_anzuelo, puntos
        img = imagenes_peces[self.tipo] # Guarda la imagen del pes
        if self.velocidad > 0:
            img = pygame.transform.flip(img, True, False) # Si avanza a la derecha, le da la vuelta a la imagen
        if self.atrapado:
            if self.velocidad > 0:
                img = pygame.transform.rotate(img, 90) # rotar la imagen del pes
            else:
                img = pygame.transform.rotate(img, -90) # rotar la imagen del pes
        screen.blit(img, self.rectangulo) # Mostrar imagen del pez
        if self.rectangulo.top < 70 and estado_anzuelo == 0:
            self.muerto = True # el objeto debe eliminarse
        if self.rectangulo.colliderect(rectangulo_anzuelo) and estado_anzuelo == 1: # verifica si esta colisonando con el anzuelo y si el anzuelo tiene carnada
            estado_anzuelo = 0 # cambia el estado del anzuelo a uno sin caranda
            puntos += 1 # suma la cantidad de puntos
            #reg_peces.remove(self) # Elimina la instancia del registro
            self.atrapado = True
        
    def Eliminar(self): # Metodo para eliminar la entidad si sobrepasa los limites
        global reg_peces, estado_anzuelo
        if self.rectangulo.left < -55 or self.rectangulo.left > 720: # Verifica que la instancia se encuentre dentro de los limites
            reg_peces.remove(self) # Elimina la instancia del registro
        if self.muerto:
            reg_peces.remove(self) # Elimina la instancia del registro
            estado_anzuelo = 1

    def movimiento(self, rectangulo_anzuelo): # Metodo para mover la imagen
        if self.atrapado:
            self.rectangulo.top = rectangulo_anzuelo.top # actualiza la posicion del rectangulo a la posicion en Y del mouse
            self.rectangulo.left = rectangulo_anzuelo.left # actualiza la posicion del rectangulo a la posicion en X del mouse
        else:
            self.rectangulo.left += 2*self.velocidad # Aumenta o reduce la pocision en X dependiento de la velocidad


#--------Ciclo de actuializacion de pantalla --------------------------------------------------------------------
def Main():

    # -------------------------Variables de configuracion-----------------
    color = 255, 255, 255 # Color de fondo base
    c = 25,25,25
    size = (720, 480) # Tamaño de la ventana
    fuente = pygame.font.match_font('arial') # fuente arial
    frecuencia = 1 # frecuencia de generacion de los peces en segundos
    pantalla = 1 # Pantalla de inicio (inicio, juego, resumen....)
    precionado = False # Variable que registra si esta o no presionado el boton de jugar
    reloj = pygame.time.Clock()
    fps = 30 # Fps del juego

    # -------------------------Cargar las imagenes------------------------ 
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
    img_anzuelo = [pygame.image.load("images/canna.png"), pygame.image.load("images/canna_carnada.png")] # Carga imagen de anzuelo vacio (0) y con carnada (1)
    rectangulo_anzuelo = img_anzuelo[0].get_rect() # obtiene el rectangulo del anzuelo

    # -----------------------Iniciar las ventanas--------------------------
    screen = pygame.display.set_mode(size) # Iniciar la ventana
    pygame.display.set_caption("Juego de pesca") # Cambiar nombre de la ventana

    while pantalla == 1:
        reloj.tick(fps) # Velocidad a la que corre el juego

        for event in pygame.event.get(): # Detecta los eventos
            if event.type == pygame.QUIT: sys.exit() # Si el evento fue presionar la X, se cierra el programa

        screen.fill(color) # Rellena el fondo
        #--Las imagenes van despues de esta linea

        precionado = Crear_boton_jugar(220, 150, precionado, screen, img_boton_jugar, event)
        if precionado:
            pantalla = 2 # Cambia de pantalla

        #--Las imagenes van antes de esta linea
        pygame.display.update() # Actualiza la imagen de la ventana



    anz = Anzuelo(rectangulo_anzuelo, img_anzuelo) # Crea una instancia del anzuelo

    Reproducir_musica("sounds/background_music.wav", 0.6, 1) # Musica de fondo

    #-------- Ciclo de actualizacion de pantalla de juego----------------------------------------------------
    while pantalla == 2:
        reloj.tick(fps) # Velocidad a la que corre el juego
        pygame.mouse.set_visible(0) # Desaparece el puntero

        for event in pygame.event.get(): # Detecta los eventos
            if event.type == pygame.QUIT: sys.exit() # Si el evento fue presionar la X, se cierra el programa

        screen.fill(color) # Rellena el fondo
        #--Las imagenes van despues de esta linea------------------------------

        screen.blit(img_fondo_mar, (0, 0)) # Mostrar fondo "mar"

        Generar_peces(frecuencia, imagenes_peces) # Se generan los peces

        muestra_texto(str(puntos), 48, 360, 20, screen, fuente) # Muestra el texto de la puntuacion

        ind_registro = len(reg_peces) - 1 # Indice del registro
        while ind_registro != -1: # Actualiza los metodos de cada instancia "peces"
            reg_peces[ind_registro].movimiento(rectangulo_anzuelo) # Llama a la funcion para mover el pez
            reg_peces[ind_registro].mos(imagenes_peces, screen, rectangulo_anzuelo) # llama a la funcion para visualizar el pez
            reg_peces[ind_registro].Eliminar() # Elimina la intancia si es necesario
            ind_registro -= 1 # Disminuye en uno el numero de indices
        
        anz.mostrar(rectangulo_anzuelo, img_anzuelo, screen, estado_anzuelo) # muestra el anzuelo en la pantalla


        #--Las imagenes van antes de esta linea---------------------------------
        pygame.display.update() # Actualiza la imagen de la ventana

Main() # Llamar a la funcion principal
