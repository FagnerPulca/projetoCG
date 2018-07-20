import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random

class Cube(object):
    def __init__(self, posicao):
        self.posicao = posicao

    
    def desenhar(self):
        
        verticies = (
            
            (-1+self.posicao[0],-1+self.posicao[1],1+self.posicao[2]),
            (1+self.posicao[0],-1+self.posicao[1],1+self.posicao[2]),
            (1+self.posicao[0],1+self.posicao[1],1+self.posicao[2]),
            (-1+self.posicao[0],1+self.posicao[1],1+self.posicao[2]),

            (1+self.posicao[0],-1+self.posicao[1],-1+self.posicao[2]),
            (-1+self.posicao[0],-1+self.posicao[1],-1+self.posicao[2]),
            (-1+self.posicao[0],1+self.posicao[1],-1+self.posicao[2]),
            (1+self.posicao[0],1+self.posicao[1],-1+self.posicao[2])
            
            )

        edges = (
            #tras
            (4,5),
            (6,7),

            #frente
            (0,1),
            (2,3),

            #lado direito
            (1,4),
            (7,2),
            
            #lado esquerdo
            (5,0),
            (3,6),

            #cima
            (3,2),
            (7,6),

            #baixo
            (5,4),
            (1,0)
    
            )

        texture_vertices = (

            (0,0),
            (1,0),
            (1,1),
            (0,1)
            )
        
        i = 0
        
        glBegin(GL_QUADS)
        for edge in edges:
            for vertex in edge:
                glTexCoord2f(texture_vertices[i][0], texture_vertices[i][1])
                glVertex3fv(verticies[vertex])

                i += 1
                if (i > 3):
                    i = 0
        glEnd()
        
class Map():
    def __init__(self):
        mapa = [[0,0,1,1,1,1,1,1,1],
                [1,0,1,0,1,1,0,0,1],
                [1,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,0,1]]
        self.cubos = []

        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                if (mapa[i][j] == 1):
                    cubo = Cube((i*2,0,j*2))
                    self.cubos.append(cubo)

    def desenhar(self):
        for cubo in self.cubos:
            cubo.desenhar()

#Função para carregar a textura
def loadTexture():

        textureSurface = pygame.image.load('textura_parede.jpeg') #carrega imagem da textura
        textureData = pygame.image.tostring(textureSurface,"RGBA",1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()

        glEnable(GL_TEXTURE_2D)#habilita textura 2D
        texid = glGenTextures(1)#ID da textura

        glBindTexture(GL_TEXTURE_2D,texid)
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,textureData)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        return texid
def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    #glTranslatef(0.0,0.0, -5)
    gluLookAt( 0.0,0.0,-2.0,
               0.0,0.0,4.0,
               0.0,-1.0,0.0)

    #Habilita o z-Buffer
    glEnable(GL_DEPTH_TEST)

    #carrega Textura
    loadTexture()
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #glRotatef(1, 3, 1, 1)
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        mapa = Map()
        mapa.desenhar()
        glPopMatrix()
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                #if (camera_x <= 5):
                glTranslatef(0.1,0,0)
            if event.key == pygame.K_d:
                glTranslatef(-0.1,0,0)
            if event.key == pygame.K_w:
                glTranslatef(0,0,0.1)
            if event.key == pygame.K_s:
                glTranslatef(0,0,-0.1)
            if event.key == pygame.K_q:
##                gluLookAt(camera_x,camera_y,camera_z, 1.0,0.0,0.0, 0.0,-1.0,0.0)
                glRotatef(3,0,-1,0)
            if event.key == pygame.K_e:
                glRotatef(3,0,1,0)
        
        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]
##        print camera_x
        
        pygame.display.flip()
        pygame.time.wait(10)


main()
