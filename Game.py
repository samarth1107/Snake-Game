import pygame
import pygame.freetype
from numpy import loadtxt
import time
import sys


#Constants for the game
WIDTH, HEIGHT = (32, 32)
#moving direction for pacman
DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)
NOTHING = (0,0)



#Draws image for the wall
def draw_wall(screen, pos):
	pixels = pixels_from_points(pos)
	screen.blit(wall,(pixels))


#Draws image for the player
def draw_pacman(screen, pos): 
	pixels = pixels_from_points(pos)
	screen.blit(pacman,(pixels))

#Draws coin image for the coin
def draw_coin(screen, pos):
	pixels = pixels_from_points(pos)
	x,y=pixels
	x=x+4
	y=y+4
	screen.blit(coin,(x,y))

#Uitlity functions
def add_to_pos(pos, pos2):
	return (pos[0]+pos2[0], pos[1]+pos2[1])

#to get pixel from points
def pixels_from_points(pos):
	return (pos[0]*WIDTH, pos[1]*HEIGHT)

#this variable will keep track of direction of ghost or enemy
loop=[0,0,0,0,0,0]
#to draw enemy vertically
def draw_enemy_vertical(screen,pos):	
	pos=tuple(pos)
	pixels = pixels_from_points(pos)
	screen.blit(ghost,(pixels))

#to get next position of enemy in the vertical position 
def enemy_vertical_pos(pos,start,end,num):
	global loop
	pos=list(pos)
	if pos[1]>end[1] and loop[num]==0:
		step=-1
	elif pos[1]==start[1]:
		loop[num]=0
		step=-1
	elif pos[1]>end[1] and loop[num]==1 :
		step=+1
	elif pos[1]==end[1]:
		loop[num]=1
		step=+1		
	pos[1]=pos[1]+step		
	return pos

#to draw enemy horizontally
def draw_enemy_horizontal(screen,pos):	
	pos=tuple(pos)
	pixels = pixels_from_points(pos)
	screen.blit(ghost,(pixels))	

#to get position of ghost or enemy in the horizontal direction	
def enemy_horizontal_pos(pos,start,end,num):
	global loop
	pos=list(pos)
	if pos[0]<end[0] and loop[num]==0:
		step=+1
	elif pos[0]==start[0]:
		loop[num]=0
		step=+1
	elif pos[0]<end[0] and loop[num]==1 :
		step=-1
	elif pos[0]==end[0]:
		loop[num]=1
		step=-1		
	pos[0]=pos[0]+step		
	return pos


#Initializing pygame
pygame.init()
screen = pygame.display.set_mode((640,700), 0, 32)
background = pygame.surface.Surface((700,700)).convert()
#this will define the font on the screen 
myfont=pygame.font.SysFont('Comic Sans MS',20)
#to load wall image
wall=pygame.image.load('wall.png')
#to load ghost image
ghost=pygame.image.load('ghost.png')
#to load coin image
coin=pygame.image.load('coin.png')
#to load pacman image
pacman=pygame.image.load('pacman.png')


#Initializing variables
layout = loadtxt('layout.txt', dtype=str)
rows, cols = layout.shape
pacman_position = (1,1)
background.fill((0,0,0))
score=0
time_sec=0


#initial postion of enemy
enemy_1=[1,12]
enemy_2=[17,9]
enemy_3=[6,17]
enemy_4=[10,2]
enemy_5=[1,13]

#this variable will help
step=1



# Main game loop 
while True:
	#to set move direction to NONE if any valid is not given
	move_direction=NOTHING

	#if the player collects all the coins then declares him as winner
	if score == 100:
		scoretext=myfont.render("winner winner in  "+str(time_sec)+" second",0,(0,255,0))
		#to set position of winner text on screen
		screen.blit(scoretext,(200,650))
		pygame.display.update()
		#all these condition will reset the game
		pacman_position=(1,1)
		move_direction = DOWN
		score=0
		layout = loadtxt('layout.txt', dtype=str)
		time_sec=0
		time.sleep(10)

	#to get event form pygame screen
	for event in pygame.event.get():
		#to exit from game 
		if event.type ==pygame.QUIT:
			exit()
		#to get input from keyboard
		elif event.type == pygame.KEYDOWN:
			if event.key==pygame.K_DOWN:
				move_direction = DOWN
			elif event.key==pygame.K_RIGHT:
				move_direction = RIGHT
			elif event.key==pygame.K_LEFT:
				move_direction = LEFT 
			elif event.key==pygame.K_UP:
				move_direction = TOP
			
			

	#to set background to bkack color 
	screen.blit(background, (0,0))

	#to show score
	scoretext=myfont.render("Score  is  "+str(score),0,(0,255,0))
	screen.blit(scoretext,(0,650))
	
	#to keep record of time 
	time_sec+=0.5

	#to show time 
	timetext=myfont.render("Time   is  "+str(time_sec),0,(0,255,0))
	screen.blit(timetext,(0,670))

	#to get previous position of pacman (to be use in the enemy condition)
	S_pacman_position=pacman_position
	#to get new position of pacman
	pacman_position = add_to_pos(pacman_position, move_direction)
	
	#to draw and collect coins from screen
	for col in range(cols):
		for row in range(rows):
			value = layout[row][col]			
			pos = (col, row)

			#to collect coins and mark it "." and increase score by 1
			if pacman_position==pos and value=='c':
				layout[row][col]="."
				score+=1
			
			#to not move pacman if the next postion given by user is wall
			if pacman_position==pos and value =='w':
				#set move direction to NONE
				move_direction = NOTHING
				pacman_position=S_pacman_position				
			
			#if the pacman goes out of the pygame screen
			if pacman_position[1]>20 or pacman_position[0]>20 or pacman_position<(0,0):
				#all these condition will reset the game
				pacman_position=(1,1)
				move_direction = DOWN
				score=0
				layout = loadtxt('layout.txt', dtype=str)
				scoretext=myfont.render("Try again",0,(0,255,0))
				#to set position of text on screen
				screen.blit(scoretext,(200,650))	
				time.sleep(2)			
			
			#to draw wall and coin
			if value == 'w':
				draw_wall(screen, pos)
			elif value == 'c':
				draw_coin(screen, pos)			
	

	#to draw all enemy and ghost
	draw_enemy_vertical(screen,enemy_1)
	draw_enemy_vertical(screen,enemy_2)
	draw_enemy_horizontal(screen,enemy_3)
	draw_enemy_horizontal(screen,enemy_4)
	draw_enemy_horizontal(screen,enemy_5)
	#to update the screen 
	pygame.display.update()
	
	#if pacman comes in the way of ghost or enemy
	if list(pacman_position)==enemy_1 or list(pacman_position)==enemy_2 or list(pacman_position)==enemy_3 or list(pacman_position)==enemy_4 or list(pacman_position)==enemy_5 or list(S_pacman_position)==enemy_1 or list(S_pacman_position)==enemy_2 or list(S_pacman_position)==enemy_3 or list(S_pacman_position)==enemy_4 or list(S_pacman_position)==enemy_5:
			pacman_position=(1,1)
			move_direction = DOWN
			score=score-1				
			layout = loadtxt('layout.txt', dtype=str)
			scoretext=myfont.render("Try again",0,(0,255,0))
			#to set position of text on screen
			screen.blit(scoretext,(200,650))			
			time.sleep(2)	

	#to get new position of all enemy or ghost
	enemy_1=enemy_vertical_pos(enemy_1,[1,12],[1,1],1)
	enemy_2=enemy_vertical_pos(enemy_2,[17,8],[17,4],2)
	enemy_3=enemy_horizontal_pos(enemy_3,[6,17],[14,17],3)
	enemy_4=enemy_horizontal_pos(enemy_4,[10,2],[18,2],4)
	enemy_5=enemy_horizontal_pos(enemy_5,[1,13],[18,13],5)
	
	
	#this will move pacman from extrerme left opening to extreme right opening or vice versa
	if pacman_position==(0,9):
		pacman_position=(19,9)
	elif pacman_position==(19,9):
		pacman_position=(0,9)
	
	#to draw pacman on screen
	draw_pacman(screen, pacman_position)
	#to update screen and show new elements on screen
	pygame.display.update()
	#to put computer on sleep for 0.5 second	
	time.sleep(0.5)
