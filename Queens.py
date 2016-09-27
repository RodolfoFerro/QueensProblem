#!/usr/bin/python
# -*- coding: utf-8 -*-

from QueensLib import*

# Pedimos datos:
N = int(input("Enter number of queens: "))
Q = queenSearch(N)
print("Queens' positions: ", Q)
# Para N > 32 la parte gráfica tarda en cargar,
# además de que no cabe en pantalla, por lo que
# a lo más se ilustran 32 reinas en el tablero.
if N <= 32 and N > 3:
	graphicQueens(N,Q)
