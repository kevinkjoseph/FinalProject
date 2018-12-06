# add_library('minim')
import os
path = os.getcwd()
# player = Minim(this)

img_dict={}
img_dict['Beam']=loadImage(path+"/resources/images/beam.png") #Image tile for Bomb
img_dict['Blue']=loadImage(path+"/resources/images/blue.png")
img_dict['Brick']=loadImage(path+"/resources/images/brick.png")
img_dict['Door']=loadImage(path+"/resources/images/door.png")
img_dict['Fire']=loadImage(path+"/resources/images/fire.png")
img_dict['Gun']=loadImage(path+"/resources/images/gun.png")
img_dict['Jetpack']=loadImage(path+"/resources/images/jetpack.png")
img_dict['Pipe']=loadImage(path+"/resources/images/pipe.png")
img_dict['Purple']=loadImage(path+"/resources/images/purple.png")
img_dict['Trophy']=loadImage(path+"/resources/images/trophy.png")
img_dict['Corner']=loadImage(path+"/resources/images/wall_corner.png")
img_dict['Wall']=loadImage(path+"/resources/images/wall.png")
img_dict['Dave']=loadImage(path+"/resources/images/Dave.png")

class Character:
	def __init__(self,x,y,r,img,g,roof,F,h,w):
		self.x=x
		self.y=y
		self.vx=0
		self.vy=0
		self.r=r
		self.img=img
		self.g=g #ground level
		self.roof=roof
		self.f=0
		self.F=F
		self.dir=1	#1 for right, -1 for left
		self.h=h
		self.w=w

	def update(self):
		self.gravity()
		self.x += self.vx
		self.y += self.vy
	
	def display(self):
		self.update()
		
		if self.vx!=0:
			
			self.f = (self.f+0.3)%self.F

		if self.dir > 0:
			image(self.img,self.x-self.r,self.y-self.r,self.w*4,self.h*4,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
		elif self.dir < 0:
			image(self.img,self.x-self.r,self.y-self.r,self.w*4,self.h*4,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)

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
	def __init__(self,x,y,r,img,g,roof,F,h,w):
		Character.__init__(self,x,y,r,img,g,roof,F,h,w)
		self.jump=False


	def update(self):
		
		self.gravity()
		
		if self.jump==True and self.y+self.r==self.g:
			self.vy-=5

		self.x += self.vx
		self.y += self.vy

class Platform:
	def __init__(self,x,y,n,img=img_dict['Brick'],size=16):
		self.x=x
		self.y=y
		self.n=n
		self.img=img
		self.size=size

	def display(self):
		for i in range(self.n):
			image(self.img,self.x+self.size*i,self.y)
		
class Game:
	def __init__(self,w,h):
		self.w=w
		self.h=h
		self.state="menu"
		self.pause=False

		self.platforms=[]

		self.platforms.append(Platform(200,200,4))

	def display(self):
		for i in self.platforms:
			i.display()


g=Game(512,618)
c=Dave(512,636,32,img_dict['Dave'],668,100,4,16,20) #2nd parameter should be 668-r

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
			g.display()
			c.display()
		else:
			fill(255,0,0)
			textSize(30)
			text("Paused",g.w//2,g.h//2)

def keyPressed():
	if g.state=='play':

		if keyCode==LEFT:
			c.dir=-1
			c.vx=-3
		if keyCode==RIGHT:
			c.dir=1
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