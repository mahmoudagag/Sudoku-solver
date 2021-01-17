import pygame
import time

grid =[[3, 0, 6, 5, 0, 8, 4, 0, 0], 
    [5, 2, 0, 0, 0, 0, 0, 0, 0], 
    [0, 8, 7, 0, 0, 0, 0, 3, 1], 
    [0, 0, 3, 0, 1, 0, 0, 8, 0], 
    [9, 0, 0, 8, 6, 3, 0, 0, 5], 
    [0, 5, 0, 0, 9, 0, 6, 0, 0], 
    [1, 3, 0, 0, 0, 0, 2, 5, 0], 
    [0, 0, 0, 0, 0, 0, 0, 7, 4], 
    [0, 0, 5, 2, 0, 6, 3, 0, 0]]


pygame.init()
color = (225, 198, 153)
screen = pygame.display.set_mode((540,600))
screen.fill(color)
pygame.display.set_caption('Sudoku')

font = pygame.font.Font('freesansbold.ttf',32)


def is_valid(x,y,a):
    if a in grid[x]:
        return False
    for i in range(len(grid)):
        if a == grid[i][y]:
            return False
    for i in range(3):
        for j in range(3):
            if a == grid[3*(x//3) + i][3*(y//3)+j]:
                return False
    return True


def back_track(grid,x):
    removeNumber(x[-1][0],x[-1][1])
    for k in range(x[-1][2]+1,10):
        if is_valid(x[-1][0],x[-1][1],k):
            grid[x[-1][0]][x[-1][1]] = k
            x[-1][2] = k
            drawNumber(x[-1][0],x[-1][1],x[-1][2])
            return True
    grid[x[-1][0]][x[-1][1]] = 0
    x.pop()
    return back_track(grid,x)


def drawGrid():
    blockSize = 60 #Set the size of the grid block
    for x in range(10):
        if (x%3 == 0):
            pygame.draw.line(screen, (0,0,0),(x*blockSize, 0), (x*blockSize , 540), 5)
            pygame.draw.line(screen, (0,0,0),(0, x*blockSize), (540 , x*blockSize), 5)
        else:
            pygame.draw.line(screen, (0,0,0),(x*blockSize, 0), (x*blockSize , 540), 1)
            pygame.draw.line(screen, (0,0,0),(0, x*blockSize), (540 , x*blockSize), 1)
    
    pygame.draw.rect(screen,(0,0,0),(0,540,540,60))
    pygame.draw.rect(screen,(255,255,255),(5,545,530,50))

    pygame.draw.rect(screen,(255,0,0),(12,550,96,40))
    font = pygame.font.Font('freesansbold.ttf',32)
    solve = font.render("Solve",True,(0,0,0))
    screen.blit(solve,(17,555))

def drawNumber(i,j,x):
    number = font.render(str(x),True,(0,0,0))
    screen.blit(number,((j*60)+20,(i*60)+20))

def drawerror(x):
    for i in range(x):
        pygame.draw.line(screen, (255,0,0),(500 - (i*50), 555), (530- (i*50) , 590), 5)
        pygame.draw.line(screen, (255,0,0),(530- (i*50) ,555), (500 - (i*50),590), 5)

def removeNumber(i,j):
    pygame.draw.rect(screen,[225, 198, 153],[j*60+5,i*60+5,50,50], 0)

def solvingNow(text):
    font = pygame.font.Font('freesansbold.ttf',32)
    Solve = font.render(text,True,(0,0,0))
    if text == "Solved":
        screen.blit(Solve,(200,555))
    else:
        screen.blit(Solve,(150,555))


def findkey(key):
    if key == pygame.K_1:
        return 1
    if key == pygame.K_2:
        return 2
    if key == pygame.K_3:
        return 3
    if key == pygame.K_4:
        return 4
    if key == pygame.K_5:
        return 5
    if key == pygame.K_6:
        return 6
    if key == pygame.K_7:
        return 7
    if key == pygame.K_8:
        return 8
    if key == pygame.K_9:
        return 9 

x = []
i = 0
j = 0
wrongcount = 0

running = True
algo = False
addnumber = False
solved = False
timesleep = .01
solution = [[3, 1, 6, 5, 7, 8, 4, 9, 2], 
    [5, 2, 9, 1, 3, 4, 7, 6, 8], 
    [4, 8, 7, 6, 2, 9, 5, 3, 1], 
    [2, 6, 3, 4, 1, 5, 9, 8, 7], 
    [9, 7, 4, 8, 6, 3, 1, 2, 5], 
    [8, 5, 1, 7, 9, 2, 6, 4, 3], 
    [1, 3, 8, 9, 4, 7, 2, 5, 6], 
    [6, 9, 2, 3, 5, 1, 8, 7, 4], 
    [7, 4, 5, 2, 8, 6, 3, 1, 9]]


while running:

    drawGrid()

    if wrongcount:
        drawerror(wrongcount)

    time.sleep(timesleep)

    if wrongcount==3:
        algo = True
    if grid == solution:
        solvingNow("Solved")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            z,y = event.pos 
            if (z>15 and z<105) and (y>550 and y<590):
                algo = True
            elif y<540:
                cordx = (z//60)
                cordy = (y//60)
                if grid[cordy][cordx] == 0:
                    addnumber = True
        if event.type == pygame.KEYDOWN:
            if addnumber:
                number = findkey(event.key)
                if solution[cordy][cordx] == number:
                    grid[cordy][cordx] = number
                    drawNumber(cordy,cordx,number)
                elif wrongcount < 3:
                    wrongcount += 1
                    drawerror(wrongcount)
                    pygame.display.update()
                    print(wrongcount)
                addnumber = False

    for k in range(len(grid)):
        for l in range(len(grid[0])):
            if grid[k][l] != 0:
                drawNumber(k,l,grid[k][l])

    if algo:
        if grid == solution:
            solvingNow("Solved")
        else:
            solvingNow("Solving Now...")
        check = 0
        if i == 9 and j == 0:
            i = 0
            j = 0
            solved = True
        elif j == 9:
            i += 1
            j = 0
        elif grid[i][j] == 0:
            for k in range(1,10):
                if is_valid(i,j,k):
                    grid[i][j] = k 
                    y =[i,j,k]
                    x.append(y.copy())
                    j += 1
                    check = 1
                    break
            if check == 0:
                if back_track(grid,x):
                    i = x[-1][0]
                    j = x[-1][1] + 1      
        elif grid[i][j] != 0:
            j += 1


    pygame.display.update()
