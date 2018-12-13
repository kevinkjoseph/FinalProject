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
img_dict['Purple']=loadImage(path+"/resources/images/purple_things.png")
img_dict['Trophy']=loadImage(path+"/resources/images/trophy.png")
img_dict['Corner']=loadImage(path+"/resources/images/wall_corner.png")
img_dict['Wall']=loadImage(path+"/resources/images/wall.png")
img_dict['Dave']=loadImage(path+"/resources/images/Dave64.png")
img_dict['Gem']=loadImage(path+"/resources/images/gem.png")

def CollisionDetect(a, b):
	
	# collision from left side of the block
	if (b.y+b.size >= a.y+a.r > b.y or b.y+b.size >= a.y-a.r > b.y) and a.x+a.r+a.vx > b.x and a.x-a.r < b.x:
		# print("collision")
		a.vx=0
		return True
	# collision from right side of the block
	if (b.y+b.size >= a.y+a.r > b.y or b.y+b.size >= a.y-a.r > b.y) and a.x-a.r+a.vx < b.x+b.size*b.n and a.x+a.r>b.x+b.size*b.n:
		a.vx=0
		# print("collision")
		return True		
	# collision from lower side of the block
	if (b.x <= a.x+a.r <= b.x+b.size*b.n or b.x <= a.x-a.r <= b.x+b.size*b.n) and a.y-a.r+a.vy <= b.y+b.size and a.y-a.r>b.y:
		a.vy=1
		# print("collision")
		return True

	return False 
	# testX=-1
	# testY=-1
	# if x+r+vx<x2:
	# 	testX=x2-(x+r+vx)
	# elif x-r+vx>x2+w:
	# 	testX=x2+w-(x-r+vx)

	# if y-r+vy>y2+h:
	# 	testY=(y2+h)-(y-r+vy)
	

	# distance=sqrt(testX**2+testY**2)

	# if distance<=0:
	# 	return True
	# else:
	# 	return False

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
			image(self.img,self.x-self.r-g.x,self.y-self.r,2*self.r,2*self.r,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
		elif self.dir < 0:
			image(self.img,self.x-self.r-g.x,self.y-self.r,2*self.r,2*self.r,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)

		stroke(255)
		noFill()
		ellipse(self.x-g.x,self.y,2*self.r,2*self.r)


	def gravity(self):
		if self.y+self.r < self.g:
			# self.vy+=scPx/30
			self.vy+=0.10
			if self.y+self.r+self.vy>self.g:
				self.vy=self.g-(self.y+self.r)		

		else:
			# print("here")
			self.vy=0

		for p in g.platforms:
			if self.x+self.r >= p.x and self.x-self.r <= p.x+p.n*p.size and self.r+self.y <= p.y:
				self.g=p.y
				break
			else:
				self.g=g.g

class Dave(Character):
	def __init__(self,x,y,r,img,g,F,h,w):
		Character.__init__(self,x,y,r,img,g,F,h,w)
		self.jump=False
		self.score=0
		self.lives=3
		print(self.score)

	def distanceCircle(self,x,y):
		return sqrt((self.x-x)**2+(self.y-y)**2)

	def update(self):
		# print(self.y, self.r, self.g)

		self.gravity()
		if self.jump==True and self.y+self.r==self.g:
			# self.vy-=(scPx//9)
			self.vy-=4

		# if self.x>=o.8*g.w:
		# 	g.x += 0.8+g.w


		for p in g.platforms:
			CollisionDetect(self,p)

		for gm in g.gems:
			if self.distanceCircle(gm.cx,gm.cy)<=self.r+scPx/2:
				self.score+=100
				g.gems.remove(gm)
				del gm



		self.x += self.vx
		self.y += self.vy
		# print(self.vx,self.vy)

		if self.x > g.w/2 and g.level>1:
			g.x+=self.vx
			print(self.vx)
			# for i in range(10):
			# 	g.x += g.w*0.08
			# 	time.sleep(0.01)

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
			image(self.img,(self.x-g.x)+self.size*i,self.y,self.size,self.size)

		# fill(0,255,0)
		# rect (self.x,self.y,self.n*self.size,self.size)

class Pipe(Platform):
	def __init__(self,x,y,n=1,img=img_dict['Pipe'],size=scPx):
		Platform.__init__(self,x,y,n=1,img=img_dict['Pipe'],size=scPx)



	def display(self):
		for i in range(self.n):
			image(self.img,self.x+self.size*i,self.y,self.size,self.size,0,0,16,16)

class Gem:
	def __init__(self,x,y,img=img_dict['Gem']):
		self.x=x
		self.y=y
		self.cx=x+scPx/2
		self.cy=y+scPx/2
		self.img=img

	def display(self):
		image(self.img,(self.x-g.x),self.y,scPx,scPx)
		noFill()
		ellipse(self.cx,self.cy,scPx,scPx)

class Killer:	#to be inherited by purple and revolving monster
	def __init__(self,x,y,img=img_dict['Purple']):
		self.x=x
		self.y=y
		self.img=img
		self.cx=x+scPx/2
		self.cy=y+scPx/2


	def display(self):
		image(self.img,(self.x-g.x),self.y,scPx,scPx)
		noFill()
		ellipse(self.cx,self.cy,scPx,scPx)


class Game:
	def __init__(self,w,h,g):
		self.w=w
		self.h=h
		self.state="menu"
		self.pause=False
		self.g=g
		self.x=0


		self.gems=[]
		self.platforms=[]
		self.door=[]
		self.pipe=[]
		self.killer=[]
		self.winlevel=0
		self.level=1
		self.levelChange()

	def level1(self):
		
		Platforms1=[[0,1,18],[5,6,1],[9,6,1],[13,6,1],[17,6,1],[3,4,1],[7,4,1],[11,4,1],[15,4,1],[4,8,3],[10,8,6],[10,9,1],[0,10,20]]

		for i in Platforms1:
			self.platforms.append(Platform(scPx*i[0],scPx*i[1],i[2]))

		for i in range(1,10):
			self.platforms.append(Platform(0,scPx*i,1))

		for i in range(1,10):
			self.platforms.append(Platform(18*scPx,scPx*i,1))
		
		Gems1=[[1,7],[3,3],[7,3],[11,3],[15,3],[5,5],[9,5],[13,5],[17,5]]

		for i in Gems1:
			self.gems.append(Gem(scPx*i[0],scPx*i[1]))


		self.door.append(Door(scPx*11,scPx*9))
		self.pipe.append(Pipe(scPx*1,scPx*9))
		self.killer.append(Killer(scPx*11,scPx*7))


	def level2(self):
		c.x=scPx*3
		c.y=scPx*6

		# self.g=scPx*8


		self.platforms.append(Platform(0,scPx*8,20))
		self.platforms.append(Platform(scPx*23,scPx*8,20))
		self.platforms.append(Platform(0,scPx*4,20))

		self.gems.append(Gem(scPx,scPx*7))



	def transition(self):
		self.clearlevel()
		self.platforms.append(Platform(0,scPx*5,20))
		self.platforms.append(Platform(0,scPx*7,20))
		c.x=scPx//8
		c.y=scPx*6+c.r//2
		c.vx=scPx//5
		time.sleep(4)
		self.level+=1

	def levelChange(self):

		if self.level==1:
			self.level1()
		
		if self.level==2:
			self.level2()

	def clearlevel(self):
		del self.platforms[:]
		del self.door[:]
		del self.pipe[:]

	def checkWin(self):
		if self.level==1:
			if c.x in range(scPx*11,scPx*12) and c.y in range (scPx*9,scPx*10):
				self.winlevel=1
				
				self.transition()

				# self.levelChange()

	def display(self):
		


		for i in self.platforms:
			i.display()
		for i in self.door:
			i.display()
		for i in self.pipe:
			i.display()
		for i in self.gems:
			i.display()

		self.checkWin()


c=Dave(1.5*scPx+scPx/2,9*scPx+scPx/2,0.90*scPx,img_dict['Dave'],10*scPx,4,16,16)
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
			line(0,scPx*7,scPx*20,scPx*7)
			
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
			if c.x>=0:
				c.vx= -(scPx/10)
			print(g.x)
		if keyCode==RIGHT:
			c.dir=1
			c.vx= scPx/10
			print(g.x)
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
