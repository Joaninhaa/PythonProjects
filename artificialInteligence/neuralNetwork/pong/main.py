import pygame 
from random import choice, uniform, seed
import numpy as np
pygame.init()
pygame.font.init()

WHITE = (255, 255, 227)
BLACK = (5, 2, 5)

TAM = 32
RES = (25*TAM, 20*TAM)
FPS = 60
ALPHA = 0.001

# Weights Input Layer
weiInLayer1 = []
for i in range(0, 5):
  weiInLayer1.append(uniform(-1, 1))
weiInLayer1 = np.array(weiInLayer1)
  
weiInLayer2 = []
for i in range(0, 5):
  weiInLayer2.append(uniform(-1, 1))
weiInLayer2= np.array(weiInLayer2)

#Weights First Hidden Layer
weiFirHidLayer1 = []
for i in range(0, 2):
  weiFirHidLayer1.append(uniform(-1, 1))
weiFirHidLayer1= np.array(weiFirHidLayer1)

weiFirHidLayer2 = []
for i in range(0, 2):
  weiFirHidLayer2.append(uniform(-1, 1))
weiFirHidLayer2= np.array(weiFirHidLayer2)

# Weights Output Layer
weiOutLayer = []
for i in range(0, 2):
  weiOutLayer.append(uniform(-1, 1))
weiOutLayer= np.array(weiOutLayer)

# First Hidden Layer Inputs
firHidValue1 = np.array([])
firHidValue2 = np.array([])

# Second Hidden Layer Inputs
secHidValue1 = np.array([])
secHidValue2 = np.array([])




class Ball():
    def __init__(self, x=RES[0]//2, y=RES[1]//2, collideTolerance=10):
        self.tam = TAM//2
        self.collideTolerance = collideTolerance
        self.rect = pygame.Rect(x - self.tam//2, y - self.tam//2, self.tam, self.tam)
        self.velX = 4 * choice((1, -1))
        self.velY = 4 * choice((1, -1))
        self.score = 0
    
    def draw(self, surf, player, font):
        pygame.draw.rect(surf, WHITE, self.rect)
        txtPlayerScore = font.render(str(player.score), 1, WHITE)
        txtBallScore = font.render(str(self.score), 1, WHITE)
        
        surf.blit(txtPlayerScore, (RES[0]//2-TAM//2-txtPlayerScore.get_width(), 0))
        surf.blit(txtBallScore, (RES[0]//2+TAM//2, 0))
        pygame.draw.line(surf, WHITE, (RES[0]//2, 0), (RES[0]//2, RES[1]))
        
    def move(self, player, enemy, neuralNetwork, inValues):
        self.rect.x += self.velX
        self.rect.y += self.velY
        
        if self.rect.x <= 0 or self.rect.x + self.tam >= RES[0]:
            self.velX *= -1
            
            if self.rect.x > RES[0]//2:
                self.score += 1
            elif self.rect.x < RES[0]//2:
                player.score += 1
                neuralNetwork.backPropagation(((enemy.rect.y+enemy.height//2) - self.rect.y), inValues)
            
            
        if self.rect.y <= 0 or self.rect.y + self.tam >= RES[1]:
            self.velY *= -1

    
    def collide(self, player, enemy):
        blocks = [player, enemy]
        for b in blocks:
            if self.rect.colliderect(b.rect):
                if abs(self.rect.bottom - b.rect.top) < self.collideTolerance and self.velY < 0:
                    self.velY *= -1
                if abs(self.rect.top - b.rect.bottom) < self.collideTolerance and self.velY > 0:
                    self.velY *= -1
                if abs(self.rect.right - b.rect.left) < self.collideTolerance and self.velX > 0:
                    self.velX *= -1
                elif abs(self.rect.left - b.rect.right) < self.collideTolerance and self.velX < 0:
                    self.velX *= -1
                
                if b == enemy:
                  enemy.record += 1
  
    
class Player():
    def __init__(self, x=RES[0], y=RES[1]//2, vel=7):
        self.height = TAM*4
        self.width = TAM//2
        self.rect = pygame.Rect(x-self.width, y-self.height//2, self.width, self.height)
        self.vel = vel
        self.score = 0

    
    def draw(self, surf):
        pygame.draw.rect(surf, WHITE, self.rect)
    
    def move(self, keys):
        if keys[pygame.K_w] and self.rect.y - self.vel > 0:
            self.rect.y -= self.vel
        if keys[pygame.K_s] and self.rect.y + self.vel + self.height < RES[1]:
            self.rect.y += self.vel
  
    
class Enemy():
    def __init__(self, x=0, y=RES[1]//2, vel=7):
        self.height = TAM*4
        self.width = TAM//2
        self.vel = vel
        self.rect = pygame.Rect(x, y-self.height//2, self.width, self.height)
        self.maxRecord = 0
        self.record = 0
    
    def draw(self, surf):
        pygame.draw.rect(surf, WHITE, self.rect)

    def move(self, value):
        if value > .7 and self.rect.y - self.vel > 0:
            self.rect.y -= self.vel
        if value < -0.7 and self.rect.y + self.vel + self.height < RES[1]:
            self.rect.y += self.vel
    
    def setRecord(self, ball):
      if ball.rect.x <= 0 or ball.rect.x >= RES[0]:
        self.record = 0
      
      if self.record > self.maxRecord:
        self.maxRecord = self.record
      
            
class NeuralNetwork():
  def forwardPropagation(self, inValues):
    global firHidValue1, firHidValue2, secHidValue1, secHidValue2
    
    firHidValue1 = round(tanH(np.sum(np.array(inValues * weiInLayer1))),5)
    firHidValue2 = round(tanH(np.sum(np.array(inValues * weiInLayer2))),5)

    secHidValue1 = round(tanH(np.sum(np.array(firHidValue1 * weiFirHidLayer1))),5)
    secHidValue2 = round(tanH(np.sum(np.array(firHidValue1 * weiFirHidLayer2))),5)
    
    outputValue = (secHidValue1 * weiOutLayer[0]) + (secHidValue2 * weiOutLayer[1])
    
    return round(tanH(outputValue),  5)

  def backPropagation(self, erro, inValues):
    global firHidValue1, firHidValue2, secHidValue1, secHidValue2
    for i in range(np.size(weiInLayer1)):
      weiInLayer1[i] = weiInLayer1[i] + (ALPHA * inValues[i] * erro)
    for i in range(np.size(weiInLayer2)):
      weiInLayer2[i] = weiInLayer2[i] + (ALPHA * inValues[i] * erro)
      
    
    for i in range(np.size(weiFirHidLayer1)):
      weiFirHidLayer1[i] = weiFirHidLayer1[i] + (ALPHA * firHidValue1 * erro)
    for i in range(np.size(weiFirHidLayer2)):
      weiFirHidLayer2[i] = weiFirHidLayer2[i] + (ALPHA * firHidValue2 * erro)
 
    weiOutLayer[0] = weiOutLayer[0] + (ALPHA * secHidValue1 * erro)
    weiOutLayer[1] = weiOutLayer[1] + (ALPHA * secHidValue2 * erro)


    
def debug(surf, clock, font, ball, enemy):
    txtFPS = font.render(str(int(clock.get_fps())), 1, WHITE)
    txtMaxRecord = font.render("Record: " + str(enemy.maxRecord), 1, WHITE)
    txtRecordNow = font.render("Now: " + str(enemy.record), 1, WHITE)
    
    
    
    surf.blit(txtFPS, (RES[0]-txtFPS.get_width(), 0))
    surf.blit(txtMaxRecord, (0, 0))
    surf.blit(txtRecordNow, (0, txtMaxRecord.get_height()))

def tanH(x):
  return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))


def main():
    run = True
    win = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()
    myFont = pygame.font.SysFont("Comic Sans MS", TAM//2)
    
    ball = Ball()
    enemy = Enemy()
    player = Player()
    nn = NeuralNetwork()
    # InputsR
    inValues = np.array([enemy.rect.x/RES[0], enemy.rect.y/RES[1], ball.rect.x/RES[0], ball.rect.y/RES[1], -1]) # enemyX, enemyY, ballX, ballY, bias
    
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: run = False
                
        #region Move
        keys = pygame.key.get_pressed()
        player.move(keys)
        outputValue = nn.forwardPropagation(inValues)
        enemy.move(outputValue)
        ball.move(player, enemy, nn, inValues)
        ball.collide(player, enemy)
        #endregion
        enemy.setRecord(ball)
        
        if enemy.rect.y != ball.rect.y:
          nn.backPropagation(((enemy.rect.y+enemy.height//2) - ball.rect.y), inValues)
        
        
        inValues =  np.array([enemy.rect.x/RES[0], enemy.rect.y/RES[1], ball.rect.x/RES[0], ball.rect.y/RES[1], -1]) 
        #region Graphics
        win.fill(BLACK)
        debug(win, clock, myFont, ball, enemy)
        ball.draw(win, player, myFont)
        enemy.draw(win)
        player.draw(win)
        #endregion
        
    
        pygame.display.update()
        clock.tick(FPS)
        
main()