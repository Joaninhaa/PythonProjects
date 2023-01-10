import pygame
pygame.init()
pygame.font.init()
from math import sin

BLACK = (24, 20, 37)
WHITE = (255, 253, 210)
LIGHTPINK = (255, 183, 202)
PINK = (255, 0, 68)
YELLOW = (255, 245, 188)
LIGHTBLUE = (157, 249, 255)

FPS = 60
TAM = 32
RES = (TAM*25, TAM*20)

class ValueBar():
    def __init__(self):
        self.width = TAM * 10
        self.height = TAM // 3
        self.x = RES[0]//2 - self.width//2
        self.y = RES[1] - self.height * 3

        self.count = 0
        
        self.barRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.selectorRect = pygame.Rect(self.x, self.y-(TAM//2-4), TAM//2, TAM)

    def draw(self, surf):
        pygame.draw.rect(surf, YELLOW, self.barRect)
        pygame.draw.rect(surf, PINK, self.selectorRect)

    def setValue(self, keys):
        if keys[pygame.K_LEFT]:
            if self.x > self.barRect.x:
                self.x -= 1 / 2.5
        if keys[pygame.K_RIGHT]:
            if self.x < self.barRect.x + self.barRect.width:
                self.x += 1 /2.5
        
        self.selectorRect.x = int(self.x)
 
    def getValue(self):
        value = (RES[0]*(self.selectorRect.x - self.barRect.x))/320
        
        return value        

class SineWave():
    def __init__(self, x, mult):
        self.x = x 
        self.multParam = mult
        self.y = (sin(self.multParam * x) * (TAM * 5)) + RES[1]//2

        self.rect = pygame.Rect(self.x, self.y, 5, 5)
        pass
    
    def draw(self, surf):
        
        x = 0
        while x < 800:
            y = (sin(self.multParam * x) * (TAM * 5)) + RES[1]//2
            pygame.draw.rect(surf, LIGHTBLUE, pygame.Rect(x, y, 1, 1))
            x += .1
        pygame.draw.rect(surf, LIGHTPINK, self.rect)
    
    def getPos(self):
        return (self.x, self.y)



def debug(surf, font, clock):
    txtFps = font.render(str(int(clock.get_fps())), 1, WHITE)

    surf.blit(txtFps, (0,0))

def main():
    run = True
    win = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()
    myFont = pygame.font.SysFont("Comic Sans MS", TAM//2)
    valueBar = ValueBar()
    mult = .05

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        sineWave = SineWave(valueBar.getValue(), mult)

        keys = pygame.key.get_pressed()
        valueBar.setValue(keys)

        if keys[pygame.K_UP]:
            mult += 0.01
        if keys[pygame.K_DOWN]:
            mult -= 0.01


        win.fill(BLACK)
        debug(win, myFont, clock)
        valueBar.draw(win)
        sineWave.draw(win)
        pygame.display.update()
        clock.tick(FPS)

main()