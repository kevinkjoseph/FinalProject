# add_library('minim')
import os,math,time,random
path = os.getcwd()
# player = Minim(this)

scale = 2	#size of the game
scPx=16*scale

resetXY=[[scPx*2.5,scPx*9.5],[scPx*3.5,scPx*6.5]]	#default coordinates for each level

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
img_dict['Dave']=loadImage(path+"/resources/images/DaveTransparent.png")
img_dict['Gem']=loadImage(path+"/resources/images/gem.png")
img_dict['Monster']=loadImage(path+"/resources/images/MonsterTransparent.png")
img_dict['Life']=loadImage(path+"/resources/images/life.png")
img_dict['Bullet']=loadImage(path+"/resources/images/bullet1.png")
img_dict['Bullet2']=loadImage(path+"/resources/images/bullet2.png")

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
		a.vy=0
		# print("collision")
		return True

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
		self.f=2
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

	def killDisplay(self):
		self.f = (self.f+0.3)%self.F
		image(img_dict['Fire'],self.x-self.r-g.x,self.y-self.r,2*self.r,2*self.r,int(self.f)*16,0,int(self.f+1)*self.w,self.h)


		stroke(255)
		noFill()
		ellipse(self.x-g.x,self.y,2*self.r,2*self.r)

	def gravity(self):
		if self.y+self.r < self.g:
			if g.dave.jetpackActive==False:
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
		self.gunCollected=False
		self.trophyCollected=False
		self.jpCollected=False
		self.bullet=[]
		self.jetpackFuel=60*5
		self.jetpackActive=False


	def distanceCircle(self,x,y):
		return sqrt((self.x-x)**2+(self.y-y)**2)

	def update(self):

		if self.jetpackActive==True:
			self.jetpackFuel-=1
			if self.jetpackFuel<=0:
				self.jpCollected=False
				self.jetpackActive=False

		self.gravity()

		#jump
		if self.jump==True and self.y+self.r==self.g:
			self.vy-= scPx/8
			
		# if self.vy!=0:
		# 	print(self.g)

		for p in g.platforms:
			CollisionDetect(self,p)

		#collecting objects
		for gm in g.gems:
			if self.distanceCircle(gm.cx,gm.cy)<=self.r+scPx/2:
				g.score+=100
				g.gems.remove(gm)
				del gm

		for gn in g.gun:
			if self.distanceCircle(gn.cx,gn.cy)<=self.r+scPx/2:
				g.gun.remove(gn)
				del gn
				self.gunCollected=True

		for tr in g.trophy:
			if self.distanceCircle(tr.cx,tr.cy)<=self.r+scPx/2:
				g.trophy.remove(tr)
				del tr
				self.trophyCollected=True
				g.score+=1000

		for jp in g.jetpack:
			if self.distanceCircle(jp.cx,jp.cy)<=self.r+scPx/2:
				g.jetpack.remove(jp)
				del jp
				self.jpCollected=True

		#collisions with purple killer things
		for k in g.killer:
			if self.distanceCircle(k.cx,k.cy)<=self.r+scPx/2:
				image(img_dict['Fire'],self.x-self.r-g.x,self.y-self.r,2*self.r,2*self.r,0,0,16,16)
				g.lives-=1
				# print(g.lives)
				time.sleep(1.5)
				self.x=resetXY[g.level-1][0]		#resets to start of the level
				self.y=resetXY[g.level-1][1]
				self.vx=0
				self.vy=0
				self.dir=1
				self.f=2
				g.x=0	#if screen is not at beginning, it will move back

		#collisions with monsters
		for k in g.monster:
			if self.distanceCircle(k.x,k.y)<=self.r+scPx/2:
				image(img_dict['Fire'],self.x-self.r-g.x,self.y-self.r,2*self.r,2*self.r,0,0,16,16)
				g.lives-=1
				g.monster.remove(k)
				del k
				# print(g.lives)
				time.sleep(1.5)
				self.x=resetXY[g.level-1][0]		#resets to start of the level
				self.y=resetXY[g.level-1][1]
				self.vx=0
				self.vy=0
				self.dir=1
				self.f=2
				g.x=0	#if screen is not at beginning, it will move back

		for b in self.bullet:
			for m in g.monster:
				if self.x+self.r>=m.x:
					g.monster.remove(m)
					del m

		# elif self.jetpackActive==True:


		self.x += self.vx
		self.y += self.vy

		if self.x > g.w/2 and g.level>1:
			g.x+=self.vx
			# print(self.vx)

		elif self.x<g.w/2:
			g.x=0



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

class Gem:	#also to be used by the gun
	def __init__(self,x,y,img=img_dict['Gem']):
		self.x=x
		self.y=y
		self.cx=x+scPx/2
		self.cy=y+scPx/2
		self.img=img

	def display(self):
		image(self.img,(self.x-g.x),self.y,scPx,scPx)
		noFill()
		ellipse(self.cx-g.x,self.cy,scPx,scPx)

class Killer:
	def __init__(self,x,y,img=img_dict['Purple'],F=4):
		self.x=x
		self.y=y
		self.img=img
		self.cx=x+scPx/2
		self.cy=y+scPx/2
		self.f=0
		self.F=4


	def display(self):
		self.f = (self.f+0.1)%self.F
		image(self.img,self.x-g.x,self.y,scPx,scPx,int(self.f)*16,0,int(self.f+1)*16,16)

		# image(self.img,(self.x-g.x),self.y,scPx,scPx)

class Trophy(Killer):
	def __init__(self,x,y):
		Killer.__init__(self,x,y,img_dict['Trophy'],5)

class Bullet:
	def __init__(self,x,y,r=scPx*0.75,img=img_dict['Bullet'],w=scPx*0.75,h=scPx/4,vx=scPx/8,target='Enemy',owner=None):
		self.x=x
		self.y=y
		self.r=r
		self.img=img
		self.w=w
		self.h=h
		self.vx=vx
		self.target=target
		self.owner=owner
	
	def update(self):
		self.x+=self.vx
		print(self.x)

		
	def display(self):
		self.update()
		image(self.img,self.x-g.x,self.y,self.w,self.h)
		ellipse(self.x-g.x+self.w/2,self.y+self.r/2,self.r*2,self.r*2)
		
		if self.target=='Enemy':
			for m in g.monster:
				if self.x+self.r>=m.x and (m.y-m.r <= self.y <= m.y+m.r):
					g.monster.remove(m)
					del m
					g.dave.bullet.remove(self)
					del self
					g.score+=300
					return
			
			# bullet deletes if it goes off screen
			if self.x-g.x>=g.w:
				g.dave.bullet.remove(self)
				del self

		elif self.target=='Dave':
			if g.dave.distanceCircle(self.x+self.r,self.y+self.r/2)<=g.dave.r+self.r:
				print("hit dave!")
				g.lives-=1
				time.sleep(1.5)
				g.dave.x=resetXY[g.level-1][0]
				g.dave.y=resetXY[g.level-1][1]
				self.owner.mbullet=False
				self.owner.bullet.remove(self)
				del self

			elif self.x-g.x<=0:
				print("bullet left the screen to the left!")
				self.owner.mbullet=False
				self.owner.bullet.remove(self)
				del self # Simon Says-- Ask Yasir: since Monster has reference to the bullet, is "del self" ineffective?

class Monster(Character):
	def __init__(self,x,y,r,img,g,F,theta,r1):
		Character.__init__(self,x,y,r,img,g,F,21,21)
		self.theta = theta
		self.r1 = r1
		self.cx = x
		self.cy = y
		self.mbullet=False
		self.bullet=[]

	def update(self):
		self.f = (self.f+0.4)%self.F
		self.theta = self.theta + 3.5
		
		self.x = self.cx + self.r1 * cos(self.theta*PI/180)
		self.y = self.cy + self.r1 * sin(self.theta*PI/180)

		rando=random.choice([scPx*4,scPx*5,scPx*6])
		
		if self.x-g.x<=g.w and self.mbullet==False:
			# top=self.cx-self.r1
			# bottom=self.cx+self.r1-scPx
			print(self.y)
			if scPx*5<self.y<scPx*6:
				self.bullet.append(Bullet(self.x,scPx*5.5,r=scPx*0.15,img=img_dict['Bullet2'],w=scPx*0.75,h=scPx/4,vx=-(scPx/8),target='Dave',owner=self))
				print('oh nooo')

				self.mbullet=True

		for i in self.bullet:	
			print(i.x,i.y)
			i.display()
				



class Game:
	def __init__(self,w,h,g):
		self.w=w
		self.h=h
		self.state="menu"
		self.pause=False
		self.g=g
		self.x=0
		self.level=2
		self.lives=3
		self.score=0

		self.dave=Dave(1.5*scPx+scPx/2,9*scPx+scPx/2,0.90*scPx,img_dict['Dave'],10*scPx,4,16,16)
		self.gems=[]
		self.platforms=[]
		self.door=[]
		self.pipe=[]
		self.killer=[]
		self.gun=[]
		self.trophy=[]
		self.monster=[]
		self.jetpack=[]
		self.levelChange()

	def level1(self):

		self.dave.x=resetXY[0][0]
		self.dave.y=resetXY[0][1]

		#adding platforms
		Platforms1=[[0,1,18],[0,6,2],[5,6,1],[9,6,1],[13,6,1],[17,6,1],[3,4,1],[7,4,1],[11,4,1],[15,4,1],[4,8,3],[10,8,6],[10,9,1],[0,10,19]]
		Gems1=[[1,5],[3,3],[7,3],[15,3],[5,5],[9,5],[13,5],[17,5]]

		for i in Platforms1:
			self.platforms.append(Platform(scPx*i[0],scPx*i[1],i[2]))

		for i in range(1,6):
			self.platforms.append(Platform(0,scPx*i,1))
		for i in range(7,10):
			self.platforms.append(Platform(0,scPx*i,1))

		for i in range(1,10):
			self.platforms.append(Platform(18*scPx,scPx*i,1))
		
		#adding gems
		for i in Gems1:
			self.gems.append(Gem(scPx*i[0],scPx*i[1]))
		
		#adding the rest
		self.door.append(Door(scPx*11,scPx*9))
		self.pipe.append(Pipe(scPx*1,scPx*9))		
		self.killer.append(Killer(scPx*11,scPx*7))
		self.trophy.append(Trophy(scPx*11,scPx*3))

	def level2(self):
		self.clearlevel()

		self.dave.x=resetXY[1][0]
		self.dave.y=resetXY[1][1]

		BluePlatforms2=[[0,7,62],[0,3,62]]
		WallPlatforms2=[[0,1,71],[0,2,64],[70,2,2],[0,8,63],[71,8,2],[0,9,64],[70,9,2],[0,10,71],[72,7,2],[71,3,2],[71,4,20]]
		for i in range(10):
			WallPlatforms2.append([0,i+1,1])
		Killers2=[[5,6],[9,6],[13,6],[14,6],[19,6],[23,6],[27,6],[31,6],[35,6],[36,6],[40,6],[44,6],[47,6],[52,6],[53,6]]
		Fires2=[[62,7],[63,7],[63,8],[64,8],[64,9],[65,9],[68,9],[69,9],[69,8],[70,8],[70,7],[71,7]]
		Gems2=[[5,4],[14,4],[19,4],[52,4],[56,4]]

		Platforms2=[[63,5,1],[66,5,1]]

		for i in Platforms2:
			self.platforms.append(Platform(i[0]*scPx,i[1]*scPx,i[2],img_dict['Wall']))

		for i in BluePlatforms2:
			self.platforms.append(Platform(i[0]*scPx,i[1]*scPx,i[2],img_dict['Blue']))

		for i in WallPlatforms2:
			self.platforms.append(Platform(i[0]*scPx,i[1]*scPx,i[2],img_dict['Wall']))

		for i in Killers2:
			self.killer.append(Killer(i[0]*scPx,i[1]*scPx))

		for i in Fires2:
			self.killer.append(Killer(i[0]*scPx,i[1]*scPx,img_dict['Fire']))

		for i in Gems2:
			self.gems.append(Gem(i[0]*scPx,i[1]*scPx))

		self.monster.append(Monster(scPx*34,scPx*5.5,scPx,img_dict['Monster'],scPx*8,4,0,scPx))
		self.monster.append(Monster(scPx*54,scPx*5.5,scPx,img_dict['Monster'],scPx*8,4,0,scPx))
		self.gun.append(Gem(10*scPx,4*scPx,img_dict['Gun']))
		self.jetpack.append(Gem(scPx*66,scPx*9,img_dict['Jetpack']))
		self.trophy.append(Trophy(scPx*67,scPx*9))

	# def transition(self):
	# 	self.state='transition'
	# 	self.clearlevel()
	# 	self.platforms.append(Platform(0,scPx*5,20))
	# 	self.platforms.append(Platform(0,scPx*7,20))
	# 	self.platforms.append(Platform(0,scPx*6,1,img_dict['Door']))

	# 	self.dave.x=scPx*1.5
	# 	self.dave.y=scPx*6+scPx//2
	# 	self.dave.vx=4
	# 	self.x=0

	# 	if self.dave.x in range(scPx*19,scPx*20) and self.dave.y in range (scPx*6,scPx*7):
	# 		self.clearlevel()
	# 		self.level+=1

	def levelChange(self):

		if self.level==1:
			self.level1()
		
		if self.level==2:
			self.level2()

	def clearlevel(self):
		del self.platforms[:]
		del self.door[:]
		del self.pipe[:]
		del self.gems[:]
		del self.killer[:]
		del self.gun[:]
		del self.trophy[:]
		self.dave.dir=1
		self.dave.f=2
		self.trophyCollected=False
		self.gunCollected=False

	def checkWin(self):
		if self.level==1:
			if self.dave.x in range(scPx*11,scPx*12) and self.dave.y in range (scPx*9,scPx*10) and self.dave.trophyCollected==True:
				
				self.level2()
				self.level+=1

		if self.level==2:
			if self.dave.x in range(scPx*11,scPx*12) and self.dave.y in range (scPx*9,scPx*10) and self.dave.trophyCollected==True:
			
				self.clearlevel()
				g.state='Game Over'

	def display(self):
		
		self.dave.display()

		font = loadFont("8BITWONDERNominal-32.vlw")
		textAlign(LEFT, CENTER)
		textFont(font, 0.75*scPx)

		if self.dave.gunCollected==True:
			text("GUN",scPx*13,scPx*11.5)
			image(img_dict['Gun'], scPx*16,scPx*11,scPx,scPx)

		if self.dave.jpCollected==True:
			text("JETPACK",scPx*4,scPx*12.5)

		for i in self.platforms:
			i.display()
		for i in self.door:
			i.display()
		for i in self.pipe:
			i.display()
		for i in self.gems:
			i.display()
		for i in self.killer:
			i.display()
		for i in self.gun:
			i.display()
		for i in self.trophy:
			i.display()
		for i in self.dave.bullet:
			i.display()
		# for i in self.dave.bullet:
		# 	i.display()
		for i in self.monster:
			i.display()
		for i in self.jetpack:
			i.display()

		text("SCORE: {0}".format(g.score),0,scPx/2)

		text("DAVES:",scPx*13,scPx/2)
		imageMode(CENTER)
		for i in range(self.lives):
			image(img_dict['Life'],scPx*(17.5+i),scPx/2,scPx,0.75*scPx)
		imageMode(CORNER)

		self.checkWin()



g=Game(20*scPx,13*scPx,10*scPx)


def setup():
	size(20*16*scale,13*16*scale)
	background(0)
	
def draw():	

	if g.state == "menu":
		background(0)
		textSize(36)
		
	
		text("Type the H and W hotline to start the game",g.w//2.5+10, g.h//3+40)
		
	elif g.state == "play" or g.state=='transition':
		if not g.pause:
			background(0)
			stroke(255)
			line(0,scPx*11,scPx*20,scPx*11)
			line(0,scPx*1,scPx*20,scPx*1)
			line(scPx,0,scPx,scPx*13)
			# line(0,scPx*7,scPx*20,scPx*7)
			
			g.display()
		else:
			fill(255,0,0)
			textSize(30)
			text("Paused",g.w//2,g.h//2)

def keyPressed():
	if g.state=='play' or g.state=='transition':

		if keyCode==LEFT:
			g.dave.dir=-1
			if g.dave.x>=0:
				g.dave.vx= -(scPx/12)
			# print(g.x)
		if keyCode==RIGHT:
			g.dave.dir=1
			g.dave.vx= scPx/12
			# print(g.x)
		if keyCode==UP:
			g.dave.jump=True
			if g.dave.jetpackActive==True:
				g.dave.vy-=scPx/12
		if keyCode==DOWN:
			if g.dave.jetpackActive==True:
				g.dave.vy+=scPx/12	

		#instantiate bullet when ctrl key is pressed
		if keyCode==17 and g.dave.gunCollected==True and g.dave.bullet==[]:
			g.dave.bullet.append(Bullet(g.dave.x,g.dave.y,r=0.15*scPx))
			print("bang")

		if keyCode==73 and g.dave.jpCollected==True:
			if g.dave.jetpackActive==False:
				g.dave.jetpackActive=True
			elif g.dave.jetpackActive==True:
				g.dave.jetpackActive=False

	elif g.state =='menu':
		if keyCode==57:
			g.state='play'

def keyReleased():
	if keyCode==LEFT:
		g.dave.vx=0
	if keyCode==RIGHT:
		g.dave.vx=0
	if keyCode==UP:
		g.dave.jump=False
		if g.dave.jetpackActive==True:
			g.dave.vy=0
	if keyCode==DOWN:
		if g.dave.jetpackActive==True:
			g.dave.vy=0