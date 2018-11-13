import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

import math

from copy import deepcopy


ANIRES = 100


class Shape:
	def __init__(self, vertices = [], edges = []):
		self.vertices = np.array(vertices)
		self.edges = np.array(edges)
	

	def update (self) :
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		draw(sbX)
		draw(sbY)
		draw(sbZ)
		draw(self)
		pygame.display.flip()
		pygame.time.wait(10)

	
	def vectorTransformation (self, dp) :
		shape1 = deepcopy(self)
		for i in range(len(self.vertices)) :
			shape1.vertices[i] += dp
		return shape1
	
	def matrixTransformation (self, M) :
		shape1 = deepcopy(self)
		for i in range(len(self.vertices)) :
			shape1.vertices[i] = np.dot(M, self.vertices[i])
		return shape1
	
	def linearTransition (self, shape1, k) :
		shape2 = deepcopy(self)
		for i in range(len(self.vertices)) :
			shape2.vertices[i] = (1-k)*self.vertices[i] + k*shape1.vertices[i]
		return shape2

	def translate (self, inp):
		if len(inp) == 4 :	
			dx = float(inp[1])
			dy = float(inp[2])
			dz = float(inp[3])
		elif len(inp) == 3 :
			dx = float(inp[1])
			dy = float(inp[2])
			dz = 0
		d = np.array([dx, dy, dz])
		dp = d/ANIRES
		for i in range(ANIRES) :
			self = self.vectorTransformation(dp)
			self.update()
		print(self.vertices)

	def dilate (self, inp):
		k = float(inp[1])
		kp = math.pow(k,1/ANIRES)
		Mp = np.array([[kp, 0.0, 0.0], [0.0, kp, 0.0], [0.0, 0.0, kp]])
		shape1 = deepcopy(self)
		shape2 = self.matrixTransformation(Mp)
		for i in range(ANIRES) :
			self = shape1.linearTransition(shape2,i*1.0/ANIRES)
			self.update()
		
	def rotate (self, inp) :
		theta = float(inp[1])
		vektor = str(inp[2])
		tp = theta/ANIRES
		if vektor == 'z':
			Mp = np.array([[math.cos(tp), -math.sin(tp), 0.0], [math.sin(tp), math.cos(tp), 0.0], [0.0, 0.0, 1.0]])
		elif vektor == 'y':
			Mp = np.array([[math.cos(tp), 0.0, math.sin(tp)], [0.0, 1.0, 0.0], [-math.sin(tp), 0.0, math.cos(tp)]])
		elif vektor == 'x':
			Mp = np.array([[1.0 ,0.0, 0.0], [0.0, math.cos(tp), -math.sin(tp)], [0.0, math.sin(tp), math.cos(tp)]])
		for i in range(ANIRES) :
			self.matrixTransformation(Mp)
			self.update()
	
	def reflect (self, inp) :
		param = inp[1]
		shape1 = deepcopy(self)
		if param == "x" :
			Mp = np.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]])
			shape2 = self.matrixTransformation(Mp)
		elif param == "y" :
			Mp = np.array([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
			shape2 = self.matrixTransformation(Mp)
		elif param == "y=x" :
			Mp = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
			shape2 = self.matrixTransformation(Mp)
		elif param == "y=-x" :
			Mp = np.array([[0.0, -1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
			shape2 = self.matrixTransformation(Mp)
		else :
			a = param.split(",")
			x = a[0].split("(")
			y = a[1].split(")")
			p = float(x[0])
			q = float(y[0])
			d = [p, q, 0.0]
			Mp = np.array([-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0])
			shape2 = self.vectorTransformation(-d)
			shape2 = shape2.matrixTransformation(Mp)
			shape2 = shape2.vectorTransformation(d)
		for i in range(ANIRES) :
			self = self.linearTransition(shape2,i*1.0/ANIRES)
			self.update()
		
	
	def stretch (self, inp) :
		param = inp[1]
		k = float(inp[2])
		shape1 = deepcopy(self)
		if param == "x" :
			Mp = np.array([[k, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
		elif param == "y" :
			Mp = np.array([[1.0, 0.0, 0.0], [0.0, k, 0.0], [0.0, 0.0, 1.0]])
		elif param == "z" :
			Mp = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, k]])
		shape2 = self.matrixTransformation(Mp)
		for i in range(ANIRES) :
			self = shape1.linearTransition(shape2,i*1.0/ANIRES)
			self.update()
	
	def costum (self, inp) :
		param = inp[1]
		a = float(inp[2])
		b = float(inp[3])
		c = float(inp[4])
		d = float(inp[5])
		shape1 = deepcopy(self)
		Mp = np.array([[a, b, 0.0], [c, d, 0.0], [0.0, 0.0, 1.0]])
		shape2 = matrixTransformation(shape1,Mp)
		for i in range(ANIRES) :
			self = shape1.linearTransition(shape2, i*1.0/ANIRES)
			self.update()


def initiate():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	pygame.display.set_caption("Tubes Algeo")
	gluPerspective(45, (display[0]/display[1]), 0.1, 200.0)
	glTranslatef(0.0, -3, -35.5)
	glRotatef(45, 1, 1, 0)
	glRotatef(15, -1, 0, 0)
	"""MENERIMA INPUT USER"""
	print("Welcome to 3D transformation simulator!")
	print("Bentuk apakah yang ingin anda tampilkan?")
	print("1. Kubus (3D)")
	print("2. Persegi (2D)")
	print("3. Custom (2D)")


	inp = int(input())
	if (inp == 1):
		main_object = Shape([[5.0, -5.0, -5.0],	[5.0, 5.0, -5.0],	[-5.0, 5.0, -5.0], [-5.0, -5.0, -5.0], 
							[5.0, -5.0, 5.0], [5.0, 5.0, 5.0], [-5.0, -5.0, 5.0], [-5.0, 5.0, 5.0]], 
							[[0, 1], [0, 3], [0, 4], [2, 1], [2, 3], [2, 7],
							[6, 3], [6, 4], [6, 7], [5, 1], [5, 4], [5, 7]])
	elif (inp == 2):
		main_object = Shape([[5.0, 5.0, 0], [5.0, -5.0, 0], [-5.0, -5.0, 0], [-5.0, 5.0, 0]],
							[[0,1], [1,2], [2, 3], [3,0]])
	elif (inp == 3):
		Vertices = []
		Vertex = []
		Edges = []
		Edge = []
		N = int(input("Masukkan N:"))
		for i in range(N):
			Vertex = []
			Edge = []
			inp = input().split(' ')
			Vertex.append(float(inp[0]))
			Vertex.append(float(inp[1]))
			Vertex.append(0.0)
			Vertices.append(Vertex)
			Edge.append(i)
			if i == (N-1) :
				Edge.append(0)
			else :
				Edge.append(int(i+1))
			Edges.append(Edge)
			print(Edges)
			print(Edge)
			print(Vertices)
			print(Vertex)
		main_object = Shape(Vertices, Edges)
	
	return main_object
		
def draw(main_object = Shape()):
	glBegin(GL_LINES)
	for edge in main_object.edges:
		for vertex in edge:
			glVertex3fv(main_object.vertices[vertex])
	glEnd()

sbX = Shape([[100.0, 0.0, 0.0],[-100.0, 0.0, 0.0]], [[0, 1]])
sbY = Shape([[0.0, 100.0, 0.0],[0.0, -100.0, 0.0]], [[0, 1]])
sbZ = Shape([[0.0, 0.0, 100.0],[0.0, 0.0, -100.0]], [[0, 1]])

def main():
	main_object = initiate()
	while True:
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		for event in pygame.event.get():
			pass

		
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				glRotatef(1, 0, 1, 0)
			elif event.key == K_LEFT:
				glRotatef(1,0,-1, 0)
			elif event.key == K_UP:
				glRotatef(1,-1,0, 0)
			elif event.key == K_DOWN:
				glRotatef(1,1,0, 0)
			elif event.key == K_a:
				glRotatef(1,0,0, -1)
			elif event.key == K_d:
				glRotatef(1,0,0, 1)
			else:
				pass
		
		if ((event.type == KEYDOWN) and (event.key == K_l) ):
			inp = input().split(" ")
			if (inp[0] == 'translate'):
				main_object.translate(inp)
			elif (inp[0] == 'dilate'):
				main_object.dilate(inp)
			elif (inp[0] == 'rotate'):
				main_object.rotate(inp)
			elif (inp[0] == 'reflect'):
				main_object.reflect(inp)
			elif (inp[0] == 'stretch'):
				main_object.stretch(inp)	
			elif (inp[0] == 'custom'):
				main_object.custom(inp)	
			elif (inp[0] == 'exit'):
				pygame.quit()
				quit()
			print(main_object.vertices)
			main_object.update()

			"""
			while True:
				for event in pygame.event.get():
					pass
				if (event.type == ACTIVEEVENT and event.gain == 1):
					break	
			"""

		main_object.update()

main()