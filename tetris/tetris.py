import random,time,pygame,sys
from pygame.locals import *

FPS = 25
#设置长宽高
WINDOWWIDTH=640
WINDOWHEIGHT=480
BOXSIZE=20

BOARDWIDTH = 10
BOARDHEIGHT = 20
#代表空的形状
BLANK='.'
#移动速率
MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ=0.1

#x方向的边距
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH*BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#颜色
WHITE           = (255,255,255)
GRAY            = (185,185,185)
BLACK           = (  0,  0,  0)
RED             = (155,  0,  0)
LIGHTRED        = (175,  20,  20)
GREEN           = (  0, 155,   0)
LIGHTGREEN      = ( 20, 175,  20)
BLUE            = (  0,   0, 155)
LIGHTBLUE       = ( 20,  20, 175)
YELLOW          = (155, 155,   0)
LIGHTYELLOW     = (175, 175,  20)
BORDERCOLOR     = BLUE
BGCOLOR         = BLACK
TEXTCOLOR       = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS          = (     BLUE,     GREEN,     RED,     YELLOW)
LIGHTCOLORS     = (LIGHTBLUE,LIGHTGREEN,LIGHTRED,LIGHTYELLOW)

#断言，每个颜色都有对应的亮色
assert len(COLORS) == len(LIGHTCOLORS)

#模版的宽高
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

# 形状_S（S旋转有2种）
S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

# 形状_Z（Z旋转有2种）
Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

# 形状_I（I旋转有2种）
I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

# 形状_O（O旋转只有一个）
O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

# 形状_J（J旋转有4种）
J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

# 形状_L（L旋转有4种）
L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

# 形状_T（T旋转有4种）
T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

# 定义一个数据结构存储对应的形状
PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

#函数
def main():
    global FPSCLOCK,DISPLAYSURF,BASICFONT,BIGFONT
    
    pygame.init()
    
    pygame.mixer.init()
    
    FPSCLOCK = pygame.time.Clock()
    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    #基础字体及大字体
    BASICFONT = pygame.font.Font('tetris/resources/ARBERKLEY.ttf',18)
    BIGFONT = pygame.font.Font('tetris/resources/ARBERKLEY.ttf',100)
    
    pygame.display.set_caption('Tetris')
    
    showTextScreen('Tetris')
    while True:
        if random.randint(0,1) == 0:
            pygame.mixer.music.load('tetris/resources/tetrisb.mid')
        else:
            pygame.mixer.music.load('tetris/resources/tetrisc.mid')
        pygame.mixer.music.play(-1,0.0)
        
        runGame()
        
        pygame.mixer.music.stop()
        
        showTextScreen('Game Over')
        
#out
def terminate():
    pygame.quit()
    sys.exit()
    
#检测是否有退出事件
def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)
        
#检测是否有按键按下
def checkForKeyPress():
    checkForQuit()
    
    for event in pygame.event.get([KEYDOWN,KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

#创建文本绘制对象
def makeTextObjs(text,font,color):
    surf = font.render(text,True,color)
    return surf , surf.get_rect()
#开始暂停结束
def showTextScreen(text):
    #绘制文本，直到按下任意键
    titleSurf,titleRect = makeTextObjs(text,BIGFONT,TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2),int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf,titleRect)
    
    #绘制文字
    titleSurf,titeRect = makeTextObjs(text,BIGFONT,TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3,int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf,titleRect)
    
    #绘制 press a key to play
    pressKeySurf,pressKeyRect = makeTextObjs('Press a key to play',BASICFONT , TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2) , int (WINDOWHEIGHT / 2)+ 100)
    DISPLAYSURF.blit(pressKeySurf,pressKeyRect)
    
    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()


#清空board
def getBlankBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

#随机获得一个新的方块
def getNewPiece():
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape':shape,
                'rotation':random.randint(0,len(PIECES[shape])-1),
                'x':int(BOARDWIDTH / 2 ) - int(TEMPLATEWIDTH / 2),
                'y':-2,
                'color':random.randint(0,len(COLORS)-1)}
    return newPiece
#将方块放入BOARD
def addToBoard(board,piece):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] !=BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']

#判断失败
def isOnBoard(x,y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

#判断方块是否位于合法位置
def isValidPosition(board , piece , adjX=0,adjY=0):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY<0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']] [y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX , y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

#判断是否被填满
def isCompleteLine(board , y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True

#消行
def removeCompleteLines(board):
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1
    while y >= 0:
        if isCompleteLine(board,y):
            for pullDownY in range(y , 0 , -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
        else:
            y -= 1 
    return numLinesRemoved

#提升等级
def calculateLevelAndFallFreq(score):
    level = int(score / 10 )+ 1
    fallFreq = 0.27 - (level * 0.02)
    return level,fallFreq

def runGame():
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    
    movingDown = False
    movingLeft = False
    movingRight = False
    
    score = 0
    level,fallFreq = calculateLevelAndFallFreq(score)
    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()
    
    while True:
        #检测当前是否有下落的piece
        if fallingPiece == None:
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            
            lastFallTime = time.time()
            
            if not isValidPosition(board,fallingPiece):
                return
        
        #检测是否有退出事件
        checkForQuit()
        
        #事件处理循环
        for event in pygame.event.get():
            if event.type == KEYUP:
                if(event.key == K_p):
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    
                    showTextScreen('Paused')
                    
                    pygame.mixer.music.play(-1,0.0)
                    
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                    
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False
                    
            elif event.type == KEYDOWN:
                
                if(event.key == K_LEFT or event.key == K_a) and isValidPosition(board,fallingPiece,adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()
                    
                elif(event.key == K_RIGHT or event.key == K_d) and isValidPosition(board,fallingPiece,adjX=1):
                    fallingPiece['x'] += 1 
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()
                    
                #旋转
                elif(event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1 ) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board,fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1 ) % len(PIECES[fallingPiece['shape']])
                #Q反向旋转
                elif(event.key == K_q):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1 ) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board,fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                #快速下落
                elif(event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board,fallingPiece,adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()
                    
                #空格键直接下落
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1,BOARDHEIGHT):
                        if not isValidPosition(board,fallingPiece,adjY=i):
                            break
                    fallingPiece['y'] += i-1
        if(movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board,fallingPiece,adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board,fallingPiece,adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()
        
        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board,fallingPiece,adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()
            
        #自动下降piece
        if time.time() - lastFallTime > fallFreq:
            if not isValidPosition(board,fallingPiece,adjY=1):
                addToBoard(board,fallingPiece)
                score += removeCompleteLines(board)
                level,fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                fallingPiece['y'] += 1
                lastFallTime = time.time()
                
        
        #绘制屏幕
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score , level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
#根据board的坐标转换为像素坐标
def convertToPixelCoords(boxx, boxy):
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))
    
#绘制box
def drawBox(boxx , boxy , color , pixelx=None , pixely=None):
    #使用board的坐标绘制单个Box（一个Piece有四个box）
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx,pixely = convertToPixelCoords(boxx,boxy)
    pygame.draw.rect(DISPLAYSURF,COLORS[color],(pixelx + 1,pixely + 1,BOXSIZE - 1,BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF,LIGHTCOLORS[color],(pixelx + 1,pixely + 1,BOXSIZE - 4,BOXSIZE - 4))
    
#绘制board
def drawBoard(board):
    pygame.draw.rect(DISPLAYSURF,BORDERCOLOR,(XMARGIN - 3,TOPMARGIN - 7,(BOARDWIDTH * BOXSIZE ) + 8,(BOARDHEIGHT * BOXSIZE)+ 8),5)
    pygame.draw.rect(DISPLAYSURF,BGCOLOR,(XMARGIN,TOPMARGIN,BOXSIZE * BOARDWIDTH ,BOXSIZE * BOARDHEIGHT))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x,y,board[x][y])


    
#绘制PIECE
def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # 若pixelx、pixely没有被指定，则使用piece数据结构中存储的位置
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # 绘制组成Piece的每个Box
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))
#绘制提示信息，下一个Piece
def drawNextPiece(piece):
    #绘制NEXT文本
    nextSurf = BASICFONT.render('Next:',True,TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf,nextRect)
    #绘制nextPiece
    drawPiece(piece,pixelx=WINDOWWIDTH-120,pixely=100)
    
#绘制游戏分数及等级
def drawStatus(score,level):
    #绘制分数文本
    scoreSurf = BASICFONT.render('Score: {}'.format(score) , True , TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150,20)
    DISPLAYSURF.blit(scoreSurf , scoreRect)
    
    #绘制等级文本
    levelSurf = BASICFONT.render('Level: {}'.format(level) , True , TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150,50)
    DISPLAYSURF.blit(levelSurf,levelRect)
    
    
if __name__ == "__main__":
    main()
                
    
    
        



























