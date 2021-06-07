import pygame
import random
import os
pygame.init()

bg_color = (192, 192, 192)
grid_color = (128, 128, 128)

game_width = 10 
game_height = 10  
numMine = 9 
grid_size = 32 
border = 16  
top_border = 100  
display_width = grid_size * game_width + border * 2  
display_height = grid_size * game_height + border + top_border  
gameDisplay = pygame.display.set_mode((display_width, display_height))  
timer = pygame.time.Clock()  
pygame.display.set_caption("Minesweeper")  

file_path = os.path.dirname(os.path.abspath(__file__))         
image_path = os.path.join(file_path, "Sprites")  


spr_emptyGrid = pygame.image.load(os.path.join(image_path, "empty.png")).convert_alpha()
spr_nuke = pygame.image.load(os.path.join(image_path, "nuke.png")).convert_alpha()
spr_grid = pygame.image.load(os.path.join(image_path, "Grid.png")).convert_alpha()
spr_grid1 = pygame.image.load(os.path.join(image_path, "grid1.png")).convert_alpha()
spr_grid2 = pygame.image.load(os.path.join(image_path, "grid2.png")).convert_alpha()
spr_grid3 = pygame.image.load(os.path.join(image_path, "grid3.png")).convert_alpha()
spr_grid4 = pygame.image.load(os.path.join(image_path, "grid4.png")).convert_alpha()

spr_mine = pygame.image.load(os.path.join(image_path, "mine.png")).convert_alpha()
spr_mineClicked = pygame.image.load(os.path.join(image_path, "mineClicked.png")).convert_alpha()
spr_mineFalse = pygame.image.load(os.path.join(image_path, "mineFalse.png")).convert_alpha()




grid = []  
mines = []  

class Grid:
    def __init__(self, xGrid, yGrid, type):
        self.xGrid = xGrid  
        self.yGrid = yGrid  
        self.clicked = False 
        self.mineClicked = False  
        self.mineFalse = False  
        self.nuke = False  
        self.rect = pygame.Rect(border + self.xGrid * grid_size, top_border + self.yGrid * grid_size, grid_size, grid_size)
        self.val = type  

    def flächeZeichnen(self):
        if self.mineFalse:
            gameDisplay.blit(spr_mineFalse, self.rect)
        else:
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        gameDisplay.blit(spr_mineClicked, self.rect)
                    else:
                        gameDisplay.blit(spr_mine, self.rect)
                else:
                    if self.val == 0:
                        gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(spr_grid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(spr_grid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(spr_grid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(spr_grid4, self.rect)


            else:
                if self.nuke:
                    gameDisplay.blit(spr_nuke, self.rect)
                else:
                    gameDisplay.blit(spr_grid, self.rect)

    def flächeZeigen(self):
        self.clicked = True
        if self.val == 0:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if not grid[self.yGrid + y][self.xGrid + x].clicked:
                                grid[self.yGrid + y][self.xGrid + x].flächeZeigen()
        elif self.val == -1:
            for m in mines:
                if not grid[m[1]][m[0]].clicked:
                    grid[m[1]][m[0]].flächeZeigen()

    def aktualisieren(self):
        if self.val != -1:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if grid[self.yGrid + y][self.xGrid + x].val == -1:
                                self.val += 1


def Loop():
    gameState = "Playing"  
    mineLeft = numMine
    global grid  
    grid = []
    global mines


    #Erstellen von minen
    mines = [[random.randrange(0, game_width),
              random.randrange(0, game_height)]]

    for c in range(numMine - 1):
        pos = [random.randrange(0, game_width),
               random.randrange(0, game_height)]
        same = True
        while same:
            for i in range(len(mines)):
                if pos == mines[i]:
                    pos = [random.randrange(0, game_width), random.randrange(0, game_height)]
                    break
                if i == len(mines) - 1:
                    same = False
        mines.append(pos)

    #Fläche erstellen
    for j in range(game_height):
        line = []
        for i in range(game_width):
            if [i, j] in mines:
                line.append(Grid(i, j, -1))
            else:
                line.append(Grid(i, j, 0))
        grid.append(line)

    #Fläche Aktualisieren
    for i in grid:
        for j in i:
            j.aktualisieren()

    # Hauptschleife 
    while gameState != "Exit":
        
        gameDisplay.fill(bg_color)

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                gameState = "Exit"

            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in grid:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    
                                    j.flächeZeigen()
                                   
                                    if j.nuke:
                                        mineLeft += 1
                                        j.nuke = False
                                    
                                    if j.val == -1:
                                        gameState = "Game Over"
                                        j.mineClicked = True
                                elif event.button == 3:
                                    
                                    if not j.clicked:
                                        if j.nuke:
                                            j.nuke = False
                                            mineLeft += 1
                                        else:
                                            j.nuke = True
                                            mineLeft -= 1
       
                                       
        
        w = True
        for i in grid:
            for j in i:
                j.flächeZeichnen()
                if j.val != -1 and not j.clicked:
                    w = False
        if w and gameState != "Exit":
            gameState = "Win"

        
        if gameState != "Game Over" and gameState != "Win":
            print("Wird Gespielt")
        elif gameState == "Game Over":
            print("Game Over!")
            for i in grid:
                for j in i:
                    if j.nuke and j.val != -1:
                        j.mineFalse = True
        else:
            print("You WON!")
           
       

        pygame.display.update()  
        timer.tick(10) 
Loop()
pygame.quit()
quit()