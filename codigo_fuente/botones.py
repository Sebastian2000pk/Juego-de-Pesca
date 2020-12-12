import pygame, os


def Iniciar_boton(tipo, x, y):
    imagen = pygame.image.load("images/botones/boton_"+str(tipo)+".png")
    imagen = pygame.transform.scale(imagen, (58, 58))
    return Botones(imagen, x, y, tipo)

class Botones:
    def __init__(self, imagen, x, y, tipo):
        self.direccion = tipo
        self.imagen = imagen
        self.rectangulo = self.imagen.get_rect()
        self.rectangulo.top = y
        self.rectangulo.left = x

    def Actualizar(self, screen, evento, siguiente):
        screen.blit(self.imagen, self.rectangulo)
        if evento != None:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if self.rectangulo.collidepoint(x, y):
                    siguiente = self.direccion
        return siguiente