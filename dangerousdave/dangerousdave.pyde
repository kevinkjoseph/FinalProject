# add_library('minim')
import os
path = os.getcwd()
# player = Minim(this)

class Character:
	def __init__(self,x,y,r,img,g):
		self.x=x
		self.y=y
		self.vx=0
		self.vy=0
		self.r=r
		self.img=img
		self.g=g

	def update(self):
		self.gravity()
		self.x += self.vx
		self.y += self.vy
	
	def display(self):
		self.update()
		stroke(255)
		noFill()
		ellipse(self.x,self.y-self.r,2*self.r,2*self.r)

	def gravity(self):
		if self.y+self.r < self.g:
			self.vy+=0.01
		else:
			self.vy=0	
class Dave(Character):
	def __init__(self):
		Character.__init__(self)
# class Game:

# 	def __init__(self):
# 		self.
# 		self.keyHandler = {LEFT:False, RIGHT:False, UP:False}

c=Character(512,668,50,'img',668)

def setup():
	size(1024,768)
	background(0)
	
def draw():
	background(0)
	stroke(255)
	line(0,668,1024,668)
	line(80,0,80,768)
	line(944,0,944,768)
	c.display()

def keyPressed():
	if keyCode==LEFT:
		c.vx=-3
	if keyCode==RIGHT:
		c.vx=3
	if keyCode==UP:
		c.vy=-10

def keyReleased():
	if keyCode==LEFT:
		c.vx=0
	if keyCode==RIGHT:
		c.vx=0
	if keyCode==UP:
		c.vy=0


"""
1. Make Circle for the person
2. Add velocties vx and vy and speeds and directions for him
3. Add keyboards to make him move
4. Add ground and the respective borders
5. Make Game class
6. Make person class
7. Make obstacle class