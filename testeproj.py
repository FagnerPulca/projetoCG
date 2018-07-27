#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import math
import sys

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def loadTexture(textura):

        textureSurface = pygame.image.load(textura) #carrega imagem da textura
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





class Cube(object):
    def __init__(self, posicao):
        self.posicao = posicao
        self.vertices = (
            
            (-1+self.posicao[0],-1+self.posicao[1],1+self.posicao[2]),
            (1+self.posicao[0],-1+self.posicao[1],1+self.posicao[2]),
            (1+self.posicao[0],1+self.posicao[1],1+self.posicao[2]),
            (-1+self.posicao[0],1+self.posicao[1],1+self.posicao[2]),

            (1+self.posicao[0],-1+self.posicao[1],-1+self.posicao[2]),
            (-1+self.posicao[0],-1+self.posicao[1],-1+self.posicao[2]),
            (-1+self.posicao[0],1+self.posicao[1],-1+self.posicao[2]),
            (1+self.posicao[0],1+self.posicao[1],-1+self.posicao[2])
            
            )

        self.centro_massa = ((self.vertices[0][0]+self.vertices[len(self.vertices)-1][0])/2,
                        (self.vertices[0][1]+self.vertices[len(self.vertices)-1][1])/2,
                        (self.vertices[0][2]+self.vertices[len(self.vertices)-1][2])/2)

        
        #print self.vertices,"\n "
        #print self.centro_massa
        #print "_____________________________________________________\n"
    def desenhar(self):
        
       

        self.edges = (
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
        for edge in self.edges:
            for vertex in edge:
                glTexCoord2f(texture_vertices[i][0], texture_vertices[i][1])
                glVertex3fv(self.vertices[vertex])

                i += 1
                if (i > 3):
                    i = 0
        glEnd()

class Ground(object):

    def __init__(self, posicao):
        self.posicao = posicao

    
    def desenhar(self):
        chao = (
            (-1+self.posicao[0],1+self.posicao[1],1+self.posicao[2]),
            (1+self.posicao[0],1+self.posicao[1],1+self.posicao[2]),
            (1+self.posicao[0],1+self.posicao[1],-1+self.posicao[2]),
            (-1+self.posicao[0],1+self.posicao[1],-1+self.posicao[2]),
        )

        texture_vertices = (
            (0,0),
            (1,0),
            (1,1),
            (0,1)
            )
        i = 0
        glBegin(GL_QUADS)
        for vertice in chao:
            glTexCoord2f(texture_vertices[i][0], texture_vertices[i][1])
            glVertex3fv(vertice)
            i += 1
        glEnd()


def verificarColisao(pos_x,pos_z, vet_x ,vet_z, speed, mapa, tam_lado_cubo):
    nova_x = (pos_x + vet_x*speed )
    nova_z = (pos_z + vet_z*speed )
    #print len(mapa.cubos)
    colisao = True
    for cubo in mapa.cubos:
        colisao = True
        x, y, z = cubo.centro_massa
        d = math.sqrt((x-nova_x)**2 + (z-nova_z)**2)
        #print "dist", d
        #print "x", x, "---", "z",z
        #if(abs(x-nova_x) > 2 and abs(z - nova_z) > 2 or (pos_x == 0.0 and pos_z == -2.0)):
        if(d >= tam_lado_cubo):
            colisao = False
        else:
            return colisao
           
    return colisao
    
    
class Map():
    def __init__(self):
        self.mapa =[[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,1,0,1,1,0,0,1,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,1,1,1,1,1],
                    [1,1,1,1,1,1,1,0,1,0,1,0,0,0,1],
                    [1,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
                    [1,0,0,1,1,1,1,1,1,1,1,1,1,0,1],
                    [1,0,1,1,1,1,0,0,1,0,0,0,0,0,1],
                    [1,0,1,1,1,1,1,0,1,1,1,0,1,1,1],
                    [1,0,0,1,1,1,1,0,1,0,0,0,0,0,1],
                    [1,0,0,1,1,1,0,0,1,0,1,1,1,0,1],
                    [1,1,0,1,1,1,0,0,1,0,1,0,1,0,1],
                    [1,1,0,0,1,1,0,0,1,0,1,0,0,0,1],
                    [1,1,0,0,0,0,0,0,1,0,1,1,1,1,1],
                    [1,1,0,0,0,0,0,0,1,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,0,1]]
        self.cubos = []
        self.ground = []

        
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                if (self.mapa[i][j] == 1):
                    cubo = Cube((i*2,0,j*2))
                    self.cubos.append(cubo)
                if (self.mapa[i][j] == 0):
                    ground = Ground((i*2,0,j*2))
                    self.ground.append(ground)

    def desenhar(self):

        #desenha as paredes com a textura
        tex0 = loadTexture('textura_parede.jpeg')
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,tex0)
        for cubo in self.cubos:
            cubo.desenhar()
        glDisable(GL_TEXTURE_2D)

        #desenha o chão com a textura
        tex1 = loadTexture('textura_chao.jpg')
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,tex1)
        for ground in self.ground:
            ground.desenhar()
        glDisable(GL_TEXTURE_2D)

def iluminacao(camera_x,camera_y,camera_z):
    
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    
##    lightZeroPosition = [10., 10, 6., 1.]
    lightZeroPosition = [camera_x,camera_y,camera_z, 1.]

    lightZeroColor = [0.5, 0.5, 0.5, 1]
    lightEspecular = [2., 4., 10., 1.]
    
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightEspecular)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    
    glEnable(GL_LIGHT0)



def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)


    #Carrega os audios
    trilha_sonora = pygame.mixer.Sound('trilha_sonora.ogg')
    

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0,0.0,-2.0,
              0.0,0.0,4.0,
              0.0,-1.0,0.0)

    global angle, lx, lz, x, z, speed
    #Variáveis global usadas para movimentos da camera
    angle = 0.0
    lx = 0.0
    lz = 1.0
    x = 0.0
    z = -2.0
  
    #Fração da movimentação na direção da linha de visão
    speed = 0.2
    
    #Habilita o z-Buffer
    glEnable(GL_DEPTH_TEST)

    #carrega Textura
##    loadTexture()

    #toca trilha sonora
    trilha_sonora.play()

##    glutInitDisplayMode(GLUT_DEPTH|GLUT_DOUBLE|GLUT_RGBA)
    #iluminacao()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(pygame.quit())
                 
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        mapa = Map()
        mapa.desenhar()
        
        glPopMatrix()
        
        
        if event.type == pygame.KEYDOWN:
            f = glGetDoublev(GL_MODELVIEW_MATRIX)
            camera_x = f[3][0]
            camera_y = f[3][1]
            camera_z = f[3][2]
        
            #print camera_x,",",camera_z
            
            if event.key == pygame.K_UP:
                global lx, lz, x, z, speed, play_x, play_z
                #movimentação na direção da linha de visão (sentido Frente)
                #print mapa.mapa[0][3]
                if not verificarColisao(x, z, lx, lz, speed, mapa, 1.35):
                    x += lx * speed
                    z += lz * speed

                
                #print camera_x,",",camera_z
                
                #print play_x,",",play_z
                
            if event.key == pygame.K_DOWN:
                global lx, lz, x, z, speed
                
                #movimentação na direção da linha de visão (sentido Trás)
                if not verificarColisao(x, z, -lx, -lz, speed, mapa, 1.35):
                    x -= lx * speed 
                    z -= lz * speed
                #print camera_x,",",camera_z
            if event.key == pygame.K_LEFT:
                global lx, lz, angle
                #Rotaciona a linha de visão em a esquerda
                
                angle -= 0.1
                lx = math.sin(angle)
                lz = math.cos(angle)
                
                #print camera_x,",",camera_z
                
            if event.key == pygame.K_RIGHT:
                global angle, lx, lz
                #Rotaciona a linha de visão em a direita
                angle += 0.1
                lx = math.sin(angle)
                lz = math.cos(angle)
                #print camera_x,",",camera_z

            iluminacao(x + lx + 2,camera_y,z + lz + 2)

        # Reset transformations
        glLoadIdentity()
	# Set the camera
        gluLookAt(x, 0.0, z,  x+lx, 0.0, z+lz,  0.0, -1.0,  0.0)
            
        pygame.display.flip()
        pygame.time.wait(5)


if __name__ =="__main__":
    main()
