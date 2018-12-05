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
		ellipse(self.x,self.y,2*self.r,2*self.r)

	def gravity(self):
		if self.y+self.r < self.g:
			self.vy+=0.08
			if self.y+self.r+self.vy>self.g:
				self.vy=self.g-(self.y+self.r)
		else:
			self.vy=0

class Dave(Character):
	def __init__(self,x,y,r,img,g):
		Character.__init__(self,x,y,r,img,g)
		self.jump=False

	def update(self):
		
		self.gravity()
		
		if self.jump==True and self.y+self.r==self.g:
			self.vy-=5

		self.x += self.vx
		self.y += self.vy
		
class Game:
	def __init__(self,w,h):
		self.w=w
		self.h=h
		self.state="menu"
		self.pause=False

g=Game(512,618)
c=Dave(512,618,50,'img',668)

def setup():
	size(1024,768)
	background(0)
	
def draw():
	if g.state == "menu":
		background(0)
		textSize(36)
		
	
		text("Type the H and W hotline to start the game",g.w//2.5+10, g.h//3+40)
		
	elif g.state == "play":
		if not g.pause:
			background(0)
			stroke(255)
			line(0,668,1024,668)
			line(80,0,80,768)
			line(944,0,944,768)
			c.display()
		else:
			fill(255,0,0)
			textSize(30)
			text("Paused",g.w//2,g.h//2)

def keyPressed():
	if g.state=='play':

		if keyCode==LEFT:
			c.vx=-3
		if keyCode==RIGHT:
			c.vx=3
		if keyCode==UP:
			c.jump=True
	elif g.state =='menu':
		if keyCode==57:
			g.state='play'

def keyReleased():
	if keyCode==LEFT:
		c.vx=0
	if keyCode==RIGHT:
		c.vx=0
	if keyCode==UP:
		c.jump=False


"""
1. Make Circle for the person
2. Add velocties vx and vy and speeds and directions for him
3. Add keyboards to make him move
4. Add ground and the respective borders
5. Make Game class
6. Make person class
7. Make obstacle class