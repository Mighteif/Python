import random,sys,time,pygame
from pygame.locals import *



FPS=5




#屏幕大小与最小像素点
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

#做出断言保证稳定性
assert WINDOWWIDTH % CELLSIZE ==0,"window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0,"window height must be a multiple of cell size."

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
DARKGREEN=(0,155,0)
DARKGRAY =(40,40,40)
BGCOLOR = BLACK

#background
pygame.mixer.init()
pygame.mixer.music.load('snake/sound/background.mp3')
pygame.mixer.music.set_volume
pygame.mixer.music.play(-1,0.0)

#sound
eat=pygame.mixer.Sound('snake/sound/eat.wav')
fail=pygame.mixer.Sound('snake/sound/fail.wav')

#定义动作
UP='up'
DOWN='down'
LEFT='left'
RIGHT='right'

HEAD = 0

def main():
	global FPSCLOCK,DISPLAYSURF,BASICFONT


	pygame.init()

	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('snake/resources/ARBERKLEY.ttf',18)
	pygame.display.set_caption('snake')
	showStartScreen()

	while True:

		runGame()
		showGameOverScreen()
		


#绘制棋盘
def drawGrid():
	for x in range(0,WINDOWWIDTH,CELLSIZE):
		pygame.draw.line(DISPLAYSURF , DARKGRAY , (x,0),(x,WINDOWHEIGHT))
	for y in range(0,WINDOWHEIGHT,CELLSIZE):
		pygame.draw.line(DISPLAYSURF , DARKGRAY , (0,y),(WINDOWWIDTH,y))


#随机生成食物位置
def getRandomLocation():
	return {'x':random.randint(0,CELLWIDTH - 1),'y':random.randint(0,CELLHEIGHT - 1)}

#绘制食物
def drawApple(coord):
	x = coord['x'] * CELLSIZE
	y = coord['y'] * CELLSIZE
	appleRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
	pygame.draw.rect(DISPLAYSURF,RED,appleRect)

#根据wormcoords列表绘制蛇
def drawWorm(wormCoords):
	for coord in wormCoords:
		x = coord['x'] * CELLSIZE
		y = coord['y'] * CELLSIZE
		wormSegmentRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
		pygame.draw.rect(DISPLAYSURF,DARKGREEN,wormSegmentRect)
		wormInnerSegmentRect = pygame.Rect(x + 4,y + 4 ,CELLSIZE - 8, CELLSIZE - 8)
		pygame.draw.rect(DISPLAYSURF,GREEN,wormInnerSegmentRect)

#score
def drawScore(score):
	scoreSurf = BASICFONT.render('Score:{}'.format(score),True,WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - 120 , 10)
	DISPLAYSURF.blit(scoreSurf,scoreRect)

#exit
def terminate():
	pygame.quit()
	sys.exit()

#massage 
def drawPressKeyMsg():
	pressKeySurf = BASICFONT.render('Press a key to play.',True , DARKGRAY)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (WINDOWWIDTH - 200,WINDOWHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf,pressKeyRect)

#event
def checkForKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		terminate()
	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None
	if keyUpEvents[0].key == K_ESCAPE:
		terminate()
	return keyUpEvents[0].key

#start
def showStartScreen():
	
	DISPLAYSURF.fill(BGCOLOR)
	titleFont = pygame.font.Font('snake/resources/ARBERKLEY.ttf',100)
	titleSurf = titleFont.render('Snake!',True , GREEN)
	titleRect = titleSurf.get_rect()
	titleRect.center = (WINDOWWIDTH / 2 , WINDOWHEIGHT / 2)
	DISPLAYSURF.blit(titleSurf , titleRect)
	
	drawPressKeyMsg()
	
	pygame.display.update()
	
	while True:
		if checkForKeyPress():
			pygame.event.get()
			return

#running
def runGame():
	
	#随机初始点，随机范围为离墙壁一段距离
	startx = random.randint(5,CELLWIDTH - 6)
	starty = random.randint(5,CELLHEIGHT - 6)
	#这里是头
	#身体的建立为列表，每一段身体为一个字典
	wormCoords = [{'x':startx,'y':starty},{'x':startx-1,'y':starty},{'x':startx-2,'y':starty}]
	direction = RIGHT

	apple = getRandomLocation()

	#游戏主体循环及操作
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			#按键
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
					direction = LEFT
				elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
					direction = RIGHT
				elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
					direction = UP
				elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
					direction = DOWN
				elif event.key == K_ESCAPE:
					terminate()

#蛇头使用HEAD HEAD已被定义为0 为列表第一个字典坐标
#两种死亡可能  检测蛇头是否在墙壁，检测蛇头与蛇身是否重叠
		if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x']==CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y']==CELLHEIGHT:
			fail.play()
			return
		for wormBody in wormCoords[1:]:
			if wormBody['x']== wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
				fail.play()
				return
#检测吃到苹果
		if wormCoords[HEAD]['x']== apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
			#吃到苹果 重新生成
			eat.play()
			apple = getRandomLocation()
		else:
			#没吃到，删除尾巴 
			del wormCoords[-1]
#蛇运动数据处理  添加蛇头
		if direction == UP:
			newHead = {'x':wormCoords[HEAD]['x'],'y':wormCoords[HEAD]['y'] - 1}
		elif direction == DOWN:
			newHead = {'x':wormCoords[HEAD]['x'],'y':wormCoords[HEAD]['y'] + 1}
		elif direction == LEFT:
			newHead = {'x':wormCoords[HEAD]['x']-1,'y':wormCoords[HEAD]['y'] }
		elif direction == RIGHT:
			newHead = {'x':wormCoords[HEAD]['x']+1,'y':wormCoords[HEAD]['y'] }
		wormCoords.insert(0,newHead)
		DISPLAYSURF.fill(BGCOLOR)
		drawGrid()
		drawWorm(wormCoords)
		drawApple(apple)
		drawScore(len(wormCoords) - 3)
		pygame.display.update()
		FPSCLOCK.tick(FPS)

		

#end
def showGameOverScreen():
	gameOverFont = pygame.font.Font('snake/resources/ARBERKLEY.ttf',50)
	gameSurf = gameOverFont.render('Game',True,WHITE)
	overSurf = gameOverFont.render('Over',True,WHITE)
	gameRect = gameSurf.get_rect()
	overRect = overSurf.get_rect()
	gameRect.midtop = (WINDOWWIDTH / 2 ,WINDOWHEIGHT / 2-gameRect.height-10)
	overRect.midtop = (WINDOWWIDTH / 2 ,WINDOWHEIGHT / 2)

	DISPLAYSURF.blit(gameSurf , gameRect)
	DISPLAYSURF.blit(overSurf , overRect)
	drawPressKeyMsg()
	pygame.display.update()
	pygame.time.wait(500)
	checkForKeyPress()
	
	while True:
		if checkForKeyPress():
			pygame.event.get()
			return


if __name__ == '__main__':
	main()









































