import pygame, sys, os, botones, Login, webscraping, pyttsx3
from random import randrange, choice
pygame.init()


#-------------------------------------------------------------------------------------------------
#----------- variables ---------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

reg_cajas = [] # Almacena las intancias de las cajas de carnada
reg_peces = [] # Almacena las instancias de los peces
puntos = 0 # numero de puntos
estado_anzuelo = 1 # estados del anzuelo (0:sin carnada, 1:con carnada, 2:con pez)
start_time_ticks = pygame.time.get_ticks() # tiempo de inicio del contador para la generacion de peces
last_time_ticks = start_time_ticks # tiempo requerido inicial para generar peces es de 0 seg
start_time_ticks_caja = pygame.time.get_ticks() # tiempo de inicio del contador para la generacion de cajas
last_time_ticks_caja = start_time_ticks # tiempo requerido inicial para generar las cajas es de 0 seg
num_carnadas = 3 # cantidad de carnadas en el juego}
usuario = ''
puntos2 = 0


#-------------------------------------------------------------------------------------------------
#----------- Funciones ---------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

def Reproducir_musica(ruta, vol, num):
    pygame.mixer.music.load(ruta) # carga la musica de fondo
    pygame.mixer.music.set_volume(vol) # cambiamos el volumen
    pygame.mixer.music.play(num) # reproduce la cancion

def Generar_cajas(frecuencia, imagen):
    global last_time_ticks_caja, start_time_ticks_caja
    last_time_ticks_caja = pygame.time.get_ticks() # se le asigna al ultimo ticks, los ticks actuales
    if last_time_ticks_caja >= start_time_ticks_caja + (frecuencia*1000): # verifica si el tiempo actual es mayor al tiempo inicial mas la frecuencia
        start_time_ticks_caja = pygame.time.get_ticks() # para que se inicie de nuevo el contador
        Crear_caja(imagen) # crea una instancia de las cajas

def Generar_peces(frecuencia, imagenes_peces): # funcion para generar peces
    porcentaje_peces = (0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5) # Defina la cantidad de vecez que puede aparecer un pes
    global last_time_ticks, start_time_ticks
    last_time_ticks = pygame.time.get_ticks() # se le asigna al ultimo ticks, los ticks actuales
    if last_time_ticks >= start_time_ticks + (frecuencia*1000): # verifica si el tiempo actual es mayor al tiempo inicial mas la frecuencia
        start_time_ticks = pygame.time.get_ticks() # para que se inicie de nuevo el contador
        Crear_pez(choice(porcentaje_peces), imagenes_peces) # crea una instancia de los peces

def muestra_texto(texto, dimensiones, x, y, screen, fuente):
    tipo_letra = pygame.font.Font(fuente, dimensiones) # defin el tipo de letra del texto
    superficie = tipo_letra.render(texto, True, (0, 0, 0)) # crea la imagen del texto
    rectangulo = superficie.get_rect() # recupera el rectangulo de la imagen del texto
    rectangulo.centerx = x 
    rectangulo.centery = y
    screen.blit(superficie, rectangulo) # muestra la imagen del texto
    
def Crear_boton_jugar(x, y, screen, img_boton_jugar, eventos): # Funcion que crear el boton jugar
    screen.blit(img_boton_jugar, (x, y)) # Mostrar el boton jugar
    ancho = img_boton_jugar.get_width() # Ancho de la imagen
    alto = img_boton_jugar.get_height() # Alto de la imagen
    pos1 = x + 30, y + 30 # Posicion 1 del area de colision
    pos2 = x + ancho - 30, y + alto - 30 # Posicion 2 del area de colision
    mouse_pos = pygame.mouse.get_pos()
    if eventos != None:
        if eventos.type == pygame.QUIT:
            exit()
        if eventos.type == pygame.MOUSEBUTTONDOWN and eventos.button == 1 and pos1[0] < mouse_pos[0] < pos2[0] and pos1[1] < mouse_pos[1] < pos2[1]: # Verifica si se esta precionando el mouse y si esta desntro del area del boton
            return True
        else:
            return False
    else:
        return False

def Buscar_usuario(nombre):
    global posicion_usuario
    file = open("respaldo.txt", 'r')
    lineas_separadas = file.readlines()
    file.close()
    datos_usuario = []
    contador = 0
    for linea in lineas_separadas:
        linea = linea.replace('\n', '')
        linea = linea.split(':')
        if linea[0] == nombre:
            datos_usuario = linea
            posicion_usuario = contador
            break
        contador += 1
    return datos_usuario
        

def Crear_pez(t, imagenes_peces): # Funcion para crear los peces
    global reg_peces
    p = Peces(t, len(reg_peces), imagenes_peces) # crea la instancia del objeto pez
    reg_peces.append(p) # Añade la entidad al registro de peces

# Crea las cajas de carnadas-------------
def Crear_caja(imagen_caja): # Funcion para crear las cajas de carnada
    global reg_peces
    caja = Caja_carnada(imagen_caja) # Crea una instancia de la caja de carnadas
    reg_cajas.append(caja) # Almacena la instancia de la caja en el registro

def Agregar_puntaje(puntos):
    global posicion_usuario
    if puntos > int(datos_usuario[2]):
        file = open("respaldo.txt", 'r')
        lineas_separadas = file.readlines()
        file.close()
        datos = []

        for linea in lineas_separadas:
            linea = linea.replace('\n', '')
            linea = linea.split(':')
            datos.append(linea)
        
        datos[posicion_usuario][2] = str(puntos)

        Escribir_datos(datos)
        
def Escribir_datos(datos):
    file = open("respaldo.txt", 'w')
    texto = ""
    for linea in datos:
        texto += linea[0]+':'+linea[1]+':'+linea[2]+'\n'
    file.write(texto)
    file.close()

def Cortar_texto(text):
    texto = text.split()
    
    return texto

def Resetear():
    global reg_cajas, reg_peces, puntos, estado_anzuelo, start_time_ticks, last_time_ticks,start_time_ticks_caja,last_time_ticks_caja, num_carnadas

    reg_cajas = [] # Almacena las intancias de las cajas de carnada
    reg_peces = [] # Almacena las instancias de los peces
    puntos = 0 # numero de puntos
    estado_anzuelo = 1 # estados del anzuelo (0:sin carnada, 1:con carnada, 2:con pez)
    start_time_ticks = pygame.time.get_ticks() # tiempo de inicio del contador para la generacion de peces
    last_time_ticks = start_time_ticks # tiempo requerido inicial para generar peces es de 0 seg
    start_time_ticks_caja = pygame.time.get_ticks() # tiempo de inicio del contador para la generacion de cajas
    last_time_ticks_caja = start_time_ticks # tiempo requerido inicial para generar las cajas es de 0 seg
    num_carnadas = 3 # cantidad de carnadas en el juego

#-- Escoger pantalla -------------------------
def Pantalla(numero_pantalla, screen):
    configuracion_pantalla = {'reloj': pygame.time.Clock(), 'fps': 30, 'color': (255, 255, 255)}
    if numero_pantalla == 1:
        return Escena1(configuracion_pantalla, screen)
    if numero_pantalla == 2:
        return Escena2(configuracion_pantalla, screen)
    if numero_pantalla == 3:
        return Escena3(configuracion_pantalla, screen)

#-- Pantalla 1 -------------------------------
def Escena1(configuracion, screen):
    global nombre, datos_usuario
    # Variables ------------
    frase_ya = webscraping.imprimir()
    frase_ya = frase_ya.replace("\n", "")
    #frase_ya = Cortar_texto(frase_ya)
    reproducir = True
    a = 0

    datos_usuario = Buscar_usuario(nombre)
    pygame.mouse.set_visible(True)
    continuar = True
    # Cargar imagenes varias -----
    img_fondo = pygame.image.load("images/fondolobby.png")
    img_boton_jugar = pygame.image.load("images/boton_jugar.png") # Boton jugar
    img_boton_jugar = pygame.transform.scale(img_boton_jugar, (285, 125))
    img_tutorial = pygame.image.load("images/instrucciones.png")
    img_scoreboard = pygame.image.load("images/scoreboard.png")
    evento = None
    boton_info = botones.Iniciar_boton(4, 650, 10)
    boton_continuar = botones.Iniciar_boton(5, 580, 400)
    boton_score = botones.Iniciar_boton(3, 650, 90)
    # Ciclo del juego -----
    while continuar:
        for eventos in pygame.event.get(): # Detecta los eventos
            if eventos.type == pygame.QUIT: sys.exit() # Si el evento fue presionar la X, se cierra el programa
            evento = eventos
        if a == 4:
            screen.blit(img_tutorial, (10, 0))
            b = boton_continuar.Actualizar(screen, evento, 0)
            if b == 5:
                a = 0
        elif a == 3 and nombre == 'admin': 
            screen.blit(img_scoreboard, (0, 0))
            b = boton_continuar.Actualizar(screen, evento, 0)
            if b == 5:
                a = 0
            file = open("respaldo.txt", 'r')
            lineas_separadas = file.readlines()
            file.close()
            posy = 50
            for usua in lineas_separadas:
                usua = usua.replace("\n", "")
                usua = usua.split(':')
                muestra_texto(usua[0]+"  -->  "+usua[2], 28, 360, posy, screen, pygame.font.match_font('arial'))
                posy += 60

        else:
            configuracion.get('reloj').tick(configuracion.get('fps')) # Velocidad a la que corre el juego



            screen.blit(img_fondo, (0, 0))
            #screen.fill(configuracion.get('color')) # Rellena el fondo
            #--Las imagenes van despues de esta linea

            a = boton_info.Actualizar(screen, evento, 0)
            a = boton_score.Actualizar(screen, evento, a)

            muestra_texto("maximo puntaje: "+str(datos_usuario[2]), 26, 370, 50, screen, pygame.font.match_font('arial'))
            muestra_texto(str(datos_usuario[0]), 26, 50, 10, screen, pygame.font.match_font('arial'))
            #muestra_texto(frase_ya, 18, 360, 300, screen, pygame.font.match_font('arial'))

            precionado = Crear_boton_jugar(220, 150, screen, img_boton_jugar, evento)
            if precionado:
                continuar = False
                #Pantalla(2, screen) # Cambia de pantalla a pantalla de juego


            #--Las imagenes van antes de esta linea
            if reproducir:
                pygame.display.update() # Actualiza la imagen de la ventana
                locutor = pyttsx3.init()
                locutor.say(frase_ya)
                locutor.runAndWait()
                reproducir = False
        pygame.display.update()
    return 2

#-- Pantalla 2--#
def Escena2(configuracion, screen):
    global puntos2
    # -------------------------Variables de configuracion-----------------
    frecuencia_cajas = 15 # Frecuencia de aparicion de las cajas de carnadas
    continuar = True
    frecuencia = 4 # frecuencia de generacion de los peces en segundos
    siguiente = 0

    #Cargar Imagenes varias
    img_fondo_mar = pygame.image.load("images/fondo mar.png") # Fondo del mar
    img_fondo_mar = pygame.transform.scale(img_fondo_mar, (720, 480))
    img_anzuelo = [pygame.image.load("images/canna.png"), 
    pygame.image.load("images/canna_carnada.png")] # Carga imagen de anzuelo vacio (0) y con carnada (1)
    rectangulo_anzuelo = img_anzuelo[0].get_rect() # obtiene el rectangulo del anzuelo
    img_contador_carnadas = pygame.image.load("images/contador_carnada.png") # Carga imagen del contador de las carnadas
    img_caja_carnadas = pygame.image.load("images/caja_carnadas.png") # Carga la imagen de la caja de las carnadas
    img_caja_carnadas = pygame.transform.scale(img_caja_carnadas , (50, 50)) # canbia el tamaño de la caja de carnadas
    # Cargar imagenes peces
    imagenes_peces = [pygame.image.load("images/pez azul.png"), # Carga imagen de pez azul
    pygame.image.load("images/pez morado.png"), # Carga imagen de pez morado
    pygame.image.load("images/pez rojo.png"),  # Carga imagen de pez rojo
    pygame.image.load("images/pez verde.png"), # Carga imagen de pez verde
    pygame.image.load("images/pez_globo.png"), # Imagen pez globo
    pygame.image.load("images/tiburon.png")] # Imagen tiburon
    imagenes_peces[0] = pygame.transform.scale(imagenes_peces[0], (59, 53)) # Escalar la imagen pez azul
    imagenes_peces[1] = pygame.transform.scale(imagenes_peces[1], (67, 51)) # Escalar la imagen pez morado
    imagenes_peces[2] = pygame.transform.scale(imagenes_peces[2], (161, 76)) # Escalar la imagen pez rojo
    imagenes_peces[3] = pygame.transform.scale(imagenes_peces[3], (95, 61)) # Escalar la imagen pez verde
    imagenes_peces[4] = pygame.transform.scale(imagenes_peces[4], (58, 42)) # Escalar la imagen pez globo
    imagenes_peces[5] = pygame.transform.scale(imagenes_peces[5], (339, 184)) # Escalar la imagen del tiburon
    
    # Botones
    
    #boton_musica = botones.Iniciar_boton(0, 670, 10)

    Reproducir_musica("sounds/background_music.wav", 0.6, 3) # Musica de fondo
    anz = Anzuelo(rectangulo_anzuelo, img_anzuelo) # Crea una instancia del anzuelo

    while continuar:
        configuracion.get('reloj').tick(configuracion.get('fps')) # Velocidad a la que corre el juego
        pygame.mouse.set_visible(0) # Desaparece el puntero
        

        for event in pygame.event.get(): # Detecta los eventos
            if event.type == pygame.QUIT: sys.exit() # Si el evento fue presionar la X, se cierra el programa
            if event.type == 768:
                continuar = False
                siguiente = 1
                pygame.mixer.music.stop()
        screen.fill(configuracion.get('color')) # Rellena el fondo
        #--Las imagenes van despues de esta linea------------------------------


        screen.blit(img_fondo_mar, (0, 0)) # Mostrar fondo "mar"

        #boton_musica.Mostrar(screen)

        screen.blit(img_contador_carnadas, (5, 5)) # Mostrar el contador de las carnadas
        muestra_texto("x " + str(num_carnadas), 26, 60, 30, screen, pygame.font.match_font('arial')) # Mostrar el numero de carnadas

        muestra_texto(str(puntos), 48, 360, 20, screen, pygame.font.match_font('arial')) # Muestra el texto de la puntuacion

        #---------------PECES----------------#
        Generar_peces(frecuencia, imagenes_peces) # Se generan los peces
        ind_registro = len(reg_peces) - 1 # Indice del registro
        while ind_registro != -1: # Actualiza los metodos de cada instancia "peces"
            reg_peces[ind_registro].movimiento(rectangulo_anzuelo) # Llama a la funcion para mover el pez
            reg_peces[ind_registro].mos(imagenes_peces, screen, rectangulo_anzuelo) # llama a la funcion para visualizar el pez
            reg_peces[ind_registro].Eliminar() # Elimina la intancia si es necesario
            ind_registro -= 1 # Disminuye en uno el numero de indices

        #---------------CAJAS CARNADAS----------------#
        Generar_cajas(frecuencia_cajas, img_caja_carnadas) # Genera las cajas de carnadas
        ind_registro_cajas = len(reg_cajas) - 1 # Indice del registro
        while ind_registro_cajas != -1: # Actualiza los metodos de cada instancia "peces"
            reg_cajas[ind_registro_cajas].movimiento(rectangulo_anzuelo) # Llama a la funcion para mover el pez
            reg_cajas[ind_registro_cajas].mos(screen, rectangulo_anzuelo) # llama a la funcion para visualizar el pez
            reg_cajas[ind_registro_cajas].Eliminar() # Elimina la intancia si es necesario
            ind_registro_cajas -= 1 # Disminuye en uno el numero de indices
        
        anz.mostrar(rectangulo_anzuelo, img_anzuelo, screen, estado_anzuelo) # muestra el anzuelo en la pantalla

        if num_carnadas == 0: # verifica si no hay carnadas
            pygame.mixer.music.stop() # detiene la musica de fondo
            continuar = False
            siguiente = 3
            puntos2 = puntos
            Agregar_puntaje(puntos)

        #--Las imagenes van antes de esta linea---------------------------------
        pygame.display.update() # Actualiza la imagen de la ventana
    Resetear()
    return siguiente

#-- Pantalla 2--#
def Escena3(configuracion, screen):
    global puntos2

    # Cargar imagenes ---
    img_fondo_playa = pygame.image.load("images/fondo_playa.png")

    # botones----
    boton_casa = botones.Iniciar_boton(1, 250, 310)
    boton_otravez = botones.Iniciar_boton(2, 320, 310)

    continuar = True
    siguiente = 0
    evento = None
    while continuar:

        # ------- Variables --------

        configuracion.get('reloj').tick(configuracion.get('fps')) # Velocidad a la que corre el juego
        pygame.mouse.set_visible(1) # Desaparece el puntero

        for event in pygame.event.get(): # Detecta los eventos
            if event.type == pygame.QUIT: sys.exit() # Si el evento fue presionar la X, se cierra el programa
            evento = event

        screen.fill(configuracion.get('color')) # Rellena el fondo
        #--Las imagenes van despues de esta linea------------------------------

        screen.blit(img_fondo_playa, (0, 0)) # Mostrar fondo "mar"

        # botones
        siguiente = boton_casa.Actualizar(screen, evento, siguiente)
        siguiente = boton_otravez.Actualizar(screen, evento, siguiente)        


        if siguiente != 0:
            continuar = False
        muestra_texto(str(puntos2), 65, 340, 220, screen, pygame.font.match_font('arial')) # Muestra la cantidad de puntos oobtenidos


        #--Las imagenes van antes de esta linea---------------------------------
        pygame.display.update() # Actualiza la imagen de la ventana

    return siguiente



#-------------------------------------------------------------------------------------------------
#------------- Clases ----------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

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


class Caja_carnada:
    def __init__(self, imagen):
        self.imagen = imagen # Le da la imagen de la caja
        self.existe = True # define si debe eliminarse la entidad o no
        self.atrapado = False # Define si esta atrapado
        self.x = -55 # Pocision en X donde va a aparecer la caja
        self.y = 420 # Pocision en Y donde va a aparecer la caja
        self.pos_x = randrange(0, 2) # 0 o 1: izquierda o derecha
        self.velocidad = 1# 1 o -1 para la direccion de desplazamientos
        if self.pos_x == 1:
            self.x = 720 # aparece desde la derecha
            self.velocidad = -1 # se desplaza hacia la izquierda
        self.rectangulo = imagen.get_rect() # Obtiene el rectangulo de la caja
        self.rectangulo.left = self.x # posicion del rectangulo igual a la X
        self.rectangulo.top = self.y # posicion del rectangulo igual a la Y
        
    def mos(self, screen, rectangulo_anzuelo):
        global estado_anzuelo, num_carnadas
        screen.blit(self.imagen, self.rectangulo) # Mostrar imagen del pez
        if self.rectangulo.top < 70 and estado_anzuelo == 0:
            self.existe = False # el objeto debe eliminarse
            num_carnadas += 3
            self.existe = False
        if self.rectangulo.colliderect(rectangulo_anzuelo) and estado_anzuelo != 2: # verifica si esta colisonando con el anzuelo y si el anzuelo tiene carnada
            estado_anzuelo = 0 # cambia el estado del anzuelo a uno sin caranda
            #puntos += 1 # suma la cantidad de puntos
            #reg_peces.remove(self) # Elimina la instancia del registro
            self.atrapado = True

    def movimiento(self, rectangulo_anzuelo): # Metodo para mover la imagen
        if self.atrapado:
            self.rectangulo.top = rectangulo_anzuelo.top # actualiza la posicion del rectangulo a la posicion en Y del mouse
            self.rectangulo.left = rectangulo_anzuelo.left # actualiza la posicion del rectangulo a la posicion en X del mouse
        else:
            self.rectangulo.left += 2*self.velocidad # Aumenta o reduce la pocision en X dependiento de la velocidad

    def Eliminar(self): # Metodo para eliminar la entidad si sobrepasa los limites
        global estado_anzuelo
        if self.rectangulo.left < -55 or self.rectangulo.left > 720: # Verifica que la instancia se encuentre dentro de los limites
            reg_cajas.remove(self) # Elimina la instancia del registro
        if not self.existe:
            reg_cajas.remove(self) # Elimina la instancia del registro
            estado_anzuelo = 1


class Peces:
    def __init__(self, t, posA, imagenes_peces):
        self.muerto = False # define si debe borrarse o no la entidad
        self.atrapado = False
        self.posArray = posA # recupera su pocicion inicial en el array
        self.tipo = t # Tipo de pez, sirve para usarlo dentro de la variable que almacena las imagenes de los peces
        self.imagen = imagenes_peces[self.tipo]
        self.x = -self.imagen.get_size()[0] # Posicion X inicial
        self.velocidad = 1 # Velocidad de desplazamiento
        self.y = randrange(120, 440) # Definir pocision aleatoria del eje Y
        self.pos_x = randrange(0,2)
        if self.pos_x == 1:
            self.x = 700
            self.velocidad = -1 # Cambia la direccion en la que se mueve el pez
        self.rectangulo = self.imagen.get_rect() # Guarda el rectangulo de pez
        self.rectangulo.left = self.x # darle posicion al rectangulo en X
        self.rectangulo.top = self.y
        
    def Rotar(self):
        if self.velocidad > 0:
            img = pygame.transform.flip(self.imagen, True, False) # Si avanza a la derecha, le da la vuelta a la imagen
        else:
            img = self.imagen  
        if self.atrapado:
            if self.velocidad > 0:
                img = pygame.transform.rotate(self.imagen, -90) # rotar la imagen del pes
            else:
                img = pygame.transform.rotate(self.imagen, -90) # rotar la imagen del pes
               
        return img

    def mos(self, imagenes_peces, screen, rectangulo_anzuelo): # Metodo para mostrar la imagen
        global estado_anzuelo, puntos, num_carnadas
        #img = imagenes_peces[self.tipo] # Guarda la imagen del pes
        
        screen.blit(self.Rotar(), self.rectangulo) # Mostrar imagen del pez
        if self.rectangulo.top < 70 and estado_anzuelo == 2:
            self.muerto = True # el objeto debe eliminarse
            puntos += 1 # suma la cantidad de puntos globales
        if self.rectangulo.colliderect(rectangulo_anzuelo) and estado_anzuelo == 1 and num_carnadas != 0: # verifica si esta colisonando con el anzuelo y si el anzuelo tiene carnada
            #puntos += 1 # suma la cantidad de puntos
            num_carnadas -= 1 # resta un en el numero de carnadas
            #reg_peces.remove(self) # Elimina la instancia del registro
            if self.tipo != 4 and self.tipo != 5: # Verifica que no sea un pes negativo
                self.atrapado = True
                estado_anzuelo = 2
            else:
                self.velocidad *= 2.4
                estado_anzuelo = 0
        
    def Eliminar(self): # Metodo para eliminar la entidad si sobrepasa los limites
        global reg_peces, estado_anzuelo
        if self.rectangulo.left < -self.imagen.get_size()[0] and self.velocidad < 0 or self.rectangulo.left > 720 and self.velocidad > 0: # Verifica que la instancia se encuentre dentro de los limites
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



#-------------------------------------------------------------------------------------------------------------#
#-------- Funcion principal ----------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

def Main():

    # -------------------------Variables de configuracion-----------------
    size = (720, 480) # Tamaño de la ventana

    # ------------------------- Variables -------------------------------
    siguiente = 1
    juego = True
    global datos_usuario, posicion_usuario, nombre
    frase = webscraping.main()
    # ----------------------- Login --------------------------------------
    nombre = Login.pantalla_principal()
    datos_usuario = Buscar_usuario(nombre)
    


    # -----------------------Iniciar las ventanas-------------------------------------------------------------------------------------
    screen = pygame.display.set_mode(size) # Iniciar la ventana
    pygame.display.set_caption("Juego de pesca") # Cambiar nombre de la ventana

    while juego:
        siguiente = Pantalla(siguiente, screen) # pantalla principal
        if siguiente == -1:
            juego = False


Main() # Llamar a la funcion principal
