# add_library('minim')
import os,math,time
path = os.getcwd()
# player = Minim(this)

scale = 2	#size of the game
scPx=16*scale

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

def CollisionDetect(x,y,r,x2,y2,w,h):
	
	testX=0
	testY=0
	if x+r<=x2:
		testX=x2-(x+r)
	elif x+r>=x2+w:
		testX=x2+w-(x+r)

	if y+r<=y2:
		testY=y2-(y+r)
	elif y+r>=y2+h:
		testY=(y+r)-(y2+h)

	distance=sqrt(testX**2+testY**2)

	if distance<=0:
		return True
	else:
		return False

class Character:
	def __init__(self,x,y,r,img,g,F,h,w):
		self.x=x
		self.y=y
		self.vx=0
		self.vy=0
		self.r=r//2
		self.img=img
		self.g=g #ground level
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
			image(self.img,self.x-self.r,self.y-self.r,scPx,scPx,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
		elif self.dir < 0:
			image(self.img,self.x-self.r,self.y-self.r,scPx,scPx,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)

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

		for p in g.platforms:
			if self.x in range(p.x,p.x+(p.size*p.n)) and self.r+self.y <= p.y:
				self.g=p.y
				break
			else:
				self.g=g.g

class Dave(Character):
	def __init__(self,x,y,r,img,g,F,h,w):
		Character.__init__(self,x,y,r,img,g,F,h,w)
		self.jump=False


	def update(self):
		self.gravity()
		
		if self.jump==True and self.y+self.r==self.g:
			self.vy-=5

		# for p in g.platforms:
		# 	if CollisionDetect(self.x,self.y,self.r,p.x,p.y,scPx*p.n,scPx):
		# 		self.vx=0
		# 		self.vy=0



		self.x += self.vx
		self.y += self.vy
		
		

		# if CollisionDetect(self.x,self.y,self.r,scPx*7,scPx*7,scPx*10,scPx):
		# # test whether dave is above or below
		# # if self.y += self.vy
		# 	self.vx=0
		# 	self.vy=0
		# else:
		# 	self.x += self.vx
		# 	self.y += self.vy
		
class Door:
	def __init__(self,x,y,n=1,img=img_dict['Door'],size=scPx):
		self.x=x
		self.y=y
		self.n=n
		self.img=img
		self.size=size

	def display(self):
		for i in range(self.n):
			image(self.img,self.x+self.size*i,self.y,self.size,self.size)


class Platform:
	def __init__(self,x,y,n=1,img=img_dict['Brick'],size=scPx):
		self.x=x
		self.y=y
		self.n=n
		self.img=img
		self.size=size



	def display(self):
		for i in range(self.n):
			image(self.img,self.x+self.size*i,self.y,self.size,self.size)

class Pipe(Platform):
	def __init__(self,x,y,n=1,img=img_dict['Pipe'],size=scPx):
		Platform.__init__(self,x,y,n=1,img=img_dict['Pipe'],size=scPx)



	def display(self):
		for i in range(self.n):
			image(self.img,self.x+self.size*i,self.y,self.size,self.size,0,0,16,16)
		
class Game:
	def __init__(self,w,h,g):
		self.w=w
		self.h=h
		self.state="menu"
		self.pause=False
		self.g=g

		self.platforms=[]
		self.door=[]
		self.pipe=[]
		self.winlevel=0
		self.level=2
		self.levelChange()

	def level1(self):
		for i in range(1,10):
			self.platforms.append(Platform(0,scPx*i,1))

		self.platforms.append(Platform(0,scPx,19))
		
		self.platforms.append(Platform(scPx,scPx*6))
		self.platforms.append(Platform(scPx*5,scPx*6))
		self.platforms.append(Platform(scPx*9,scPx*6))
		self.platforms.append(Platform(scPx*13,scPx*6))
		self.platforms.append(Platform(scPx*18,scPx*6))
		self.platforms.append(Platform(scPx*3,scPx*4))
		self.platforms.append(Platform(scPx*7,scPx*4))
		self.platforms.append(Platform(scPx*11,scPx*4))
		self.platforms.append(Platform(scPx*15,scPx*4))
		self.platforms.append(Platform(scPx*4,scPx*8,3))
		self.platforms.append(Platform(scPx*10,scPx*8,6))
		self.platforms.append(Platform(scPx*10,scPx*9))

		self.platforms.append(Platform(0,scPx*10,20))

		for i in range(1,10):
			self.platforms.append(Platform(19*scPx,scPx*i,1))
				
		self.door.append(Door(scPx*11,scPx*9))
		self.pipe.append(Pipe(scPx*1,scPx*9))


	def level2(self):
		c.x=scPx*3
		c.y=scPx*7

		# self.platforms.append(Platform(0,scPx*10,20))
		# self.platforms.append(Platform(0,scPx*9,20))
		# self.platforms.append(Platform(0,scPx*8,20))

		self.platforms.append(Platform(0,scPx*8,20))
		self.platforms.append(Platform(0,scPx*4,20))



	def levelChange(self):
		if self.level==1:
			self.level1()
		if self.winlevel==1:
			self.clearlevel()
			self.transition()
		if self.level==2:
			self.level2()


	def transition(self):

		self.platforms.append(Platform(0,scPx*5,20))
		self.platforms.append(Platform(0,scPx*7,20))
		c.x=0
		c.y=scPx*6
		c.vx=scPx//5


	def clearlevel(self):
		del self.platforms[:]
		del self.door[:]
		del self.pipe[:]

	def checkWin(self):
		if c.x in range(scPx*11,scPx*12) and c.y in range (scPx*9,scPx*10):
			self.winlevel=1
			self.level+=1
			self.levelChange()


	def display(self):
		
		for i in self.platforms:
			i.display()
		for i in self.door:
			i.display()
		for i in self.pipe:
			i.display()
		self.checkWin()


c=Dave(3*scPx,3*scPx,scPx,img_dict['Dave'],10*scPx,4,16,20)
g=Game(20*scPx,13*scPx,10*scPx)


def setup():
	size(20*16*scale,13*16*scale)
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
			line(0,scPx*10,scPx*20,scPx*10)
			line(scPx,0,scPx,scPx*13)
			
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
