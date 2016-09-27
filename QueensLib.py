#!/usr/bin/python
# -*- coding: utf-8 -*-


import pygame, sys
from pygame.locals import *
from itertools import permutations
from numpy.random import permutation
from copy import copy
import gc

def queenSearch(N):
	"""
		Function that finds the position of the N Queens.
	"""
	# Si N es menor a 4, no hay solución:
	if N <= 3:
		print("N must be greater.")
		Queens = []
		return Queens

	rows = range(N)		# Arreglo de filas
	cols = copy(rows)	# Arreglo de columnas,
	cols = cols[::-1]		# permutación de las filas
	cols = list(permutation(cols))
	# Si N es 4, hay solución, pero no para toda
	# x, y inicial:
	if N == 4:
		# El ciclo está más detallado para N > 4,
		# revisar comentarios de ese caso:
		# Begin loop:
		loop = True
		while loop:
			gc.collect()			# Limpiamos memoria
			cols.reverse()
			for i in range(N/4):
				cols = list(permutation(cols))
			Queens = []				# Inicializamos lista vacía
			for i in range(N):
				Queens.append([rows[i],cols[i]])
			d1 = [0]*(2*N-1)
			d2 = [0]*(2*N-1)
			for q in range(N):
				d1[Queens[q][0]+Queens[q][1]] += 1
				d2[Queens[q][0]-Queens[q][1]+(N-1)] += 1
			swaps = -1
			while swaps != 0:
				swaps = 0
				for i in range(N):
					for j in range(i+1,N):
						if isAttacked(Queens[i],d1,d2,N) or isAttacked(Queens[j],d1,d2,N):
							if checkSwap(Queens[i],Queens[j],d1,d2,N):
								swap(Queens[i],Queens[j],d1,d2,N)
								swaps += 1
			loop = collisions(Queens,d1,d2,N)
		return Queens
	if N > 4:
		# Pedimos coordenadas iniciales:
		x = int(input("Enter initial x position: "))
		y = int(input("Enter initial y position: "))
		# Inicializamos las variables en caso de estar fuera de rango:
		if x > N or y > N:
			x = 0; y = 0
		# Begin loop:
		loop = True
		# El ciclo lo realizamos mientras haya colisiones en las diagonales.
		while loop:
			gc.collect()			# Limpiamos memoria
			cols.reverse()			# Revertimos el arreglo de columnas
			for i in range(int(N/4)):	# Obtenemos una nueva permutación de las columnas
				cols = list(permutation(cols))
			Queens = []
			# Actualizamos las coordenadas de las reinas:
			for i in range(N):
				Queens.append([rows[i],cols[i]])
			# Creamos los arreglos con la cantidad de reinas
			# en las diagonales:
			d1 = [0]*(2*N-1)
			d2 = [0]*(2*N-1)
			for q in range(N):
				d1[Queens[q][0]+Queens[q][1]] += 1
				d2[Queens[q][0]-Queens[q][1]+(N-1)] += 1
			# Inicializamos la posición de entrada de la reina inicial:
			for k in range(N):
				if Queens[k][0] == x:
						x_prime = k
						break
			for k in range(N):
				if Queens[k][1] == y:
						y_prime = k
						break
			swap(Queens[x_prime],Queens[y_prime],d1,d2,N)
			# Comenzamos el ciclo que encuentra las posiciones:
			swaps = -1
			while swaps != 0:
				swaps = 0
				# Nos movemos en filas y columnas:
				for i in range(N):
					if i != x:		# Fijamos la reina inicial
						for j in range(i+1,N):
							if j != x:		# Fijamos la reina inicial
								# Si hay reinas atacándose en las diagonales,
								# verificamos si al cambiarlas se reduce el número de colisiones,
								# en caso de ser así, las cambiamos, si no, no.
								if isAttacked(Queens[i],d1,d2,N) or isAttacked(Queens[j],d1,d2,N):
									if checkSwap(Queens[i],Queens[j],d1,d2,N):
										swap(Queens[i],Queens[j],d1,d2,N)
										swaps += 1
			loop = collisions(Queens,d1,d2,N)
		return Queens


def isAttacked(queen,d1,d2,N):
	"""
		Function to verify if a queen is attacked by others.
	"""
	if d1[queen[0]+queen[1]] > 1 or d2[queen[0]-queen[1]+(N-1)] > 1:
		return True
	else:
		return False

def swap(queen1,queen2,d1,d2,N):
	"""
		Function that swaps 2 Queens.
	"""
	# Quitamos las reinas de d1 y d2:
	d1[queen1[0]+queen1[1]] -= 1
	d2[queen1[0]-queen1[1]+(N-1)] -= 1
	d1[queen2[0]+queen2[1]] -= 1
	d2[queen2[0]-queen2[1]+(N-1)] -= 1
	# Movemos las reinas:
	aux = copy(queen1[1])
	queen1[1] = copy(queen2[1])
	queen2[1] = copy(aux)
	# Actualizamos d1 y d2:
	d1[queen1[0]+queen1[1]] += 1
	d2[queen1[0]-queen1[1]+(N-1)] += 1
	d1[queen2[0]+queen2[1]] += 1
	d2[queen2[0]-queen2[1]+(N-1)] += 1
	return

def checkSwap(queen1,queen2,d1,d2,N):
	"""
		Function that checks if we get less collisions by swaping queens.
	"""
	# We declare auxiliar variables:
	Q1, Q2, D1, D2 = copy(queen1), copy(queen2), copy(d1), copy(d2)
	swap(Q1,Q2,D1,D2,N)
	# We check if there are less collisions:
	for i in range(2*N-1):
		if D1[i]>d1[i] and D1[i]!=0 and d1[i]!=0  or D2[i]>d2[i] and D2[i]!=0 and d2[i]!=0:
			return False
	return True

def collisions(Q,d1,d2,N):
	"""
		Function that checks if any queen has a collision.
	"""
	for i in range(N):
		if isAttacked(Q[i],d1,d2,N):
			return True
	return False

def graphicQueens(N,Q):
	"""
		Function makes the graphic N Queens.
	"""
	queen = pygame.image.load("queen.png")

	# Initialize window size and title:
	pygame.init()
	window = pygame.display.set_mode((32*N,32*N))
	pygame.display.set_caption("Queen's Problem")
	background = pygame.image.load("chess.png")

	while True:
		# Fill background:
		window.blit(background,(0,0))
		for q in Q:
			window.blit(queen,(q[0]*32+1,q[1]*32))
		# Check events on window:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == 27:
					pygame.quit()
					sys.exit()

		# Update window:
		pygame.display.update()
