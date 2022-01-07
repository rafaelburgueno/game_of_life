#El juego de la vida
#Automatas celulares

import sys, pygame
import numpy as np
import math
import time
#import matplotlib.pyplot as plt


pygame.init()

width, height = 500, 500
#size = width, height = 600, 600
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

#definimos la contidad de celdas por eje
nxC, nyC = 100, 100

#se calcula la dimencion de las celdas segun
#la cantidad de celdas que queremos y el ancho de la pantalla
dimCW = width / nxC
dimCH = height / nyC



#screen = pygame.display.set_mode(size)


# Estructura de datos del juego
gameState = np.zeros((nxC, nyC))


# Autómata palo
gameState[5,3] = 1
gameState[5,4] = 1
gameState[5,5] = 1

# Autómata movil
gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1


# Control de la ejecucion del juego
pauseExect = False

run = True

while run:


    newGameState = np.copy(gameState)

    # Limpiamos la pantalla para que no se superpongan los estados
    screen.fill(bg)

    time.sleep(0.1)

    # Registramos eventos de teclado y raton
    ev = pygame.event.get()



    for event in ev:

        if event.type == pygame.QUIT: run = False

        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]


    #rejilla
    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:

                # Calculamos el numero de vecinos de la celda x, y
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                          gameState[(x)   % nxC, (y-1) % nyC] + \
                          gameState[(x+1) % nxC, (y-1) % nyC] + \
                          gameState[(x-1) % nxC, (y)   % nyC] + \
                          gameState[(x+1) % nxC, (y)   % nyC] + \
                          gameState[(x-1) % nxC, (y+1) % nyC] + \
                          gameState[(x)   % nxC, (y+1) % nyC] + \
                          gameState[(x+1) % nxC, (y+1) % nyC]

                # REGLA #1
                # Una célula muerta con exactamente 3 células vecinas vivas "nace"
                if gameState[x,y] == 0 and n_neigh == 3 :
                    newGameState[x,y] = 1

                # REGLA #2
                # Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3) :
                    newGameState[x,y] = 0



            # Definimos las coordenadas del poligono a partir de x e y
            poly = [( (x) * dimCW, y * dimCH),
					( (x+1) * dimCW, y * dimCH ),
					( (x+1) * dimCW, (y+1) * dimCH ),
					( (x) * dimCW, (y+1) * dimCH )]

            # Y dibujamos la celda para cada par de x e y
            if newGameState[x,y] == 0:
                pygame.draw.polygon(screen, (128,128,128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255,255,255), poly, 0)



    # Actualiza el gameState
    gameState = np.copy(newGameState)



    pygame.display.flip()

pygame.quit()
