import pygame 
from random import choice
pygame.init()
pygame.font.init()

WHITE = (255, 255, 227)
BLACK = (5, 2, 5)

TAM = 32
RES = (25*TAM, 20*TAM)
FPS = 60


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
        
    def move(self, player):
        self.rect.x += self.velX
        self.rect.y += self.velY
        
        if self.rect.x <= 0 or self.rect.x + self.tam >= RES[0]:
            self.velX *= -1
            if self.rect.x > RES[0]//2:
                self.score += 1
            elif self.rect.x < RES[0]//2:
                player.score += 1
            
            
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
  
    
class Player():
    def __init__(self, x=RES[0], y=RES[1]//2, vel=5):
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
    def __init__(self, x=0, y=RES[1]//2, vel=5):
        self.height = TAM*4
        self.width = TAM//2
        self.vel = vel
        self.rect = pygame.Rect(x, y-self.height//2, self.width, self.height)
    
    def draw(self, surf):
        pygame.draw.rect(surf, WHITE, self.rect)

    def move(self, keys):
        if keys[pygame.K_UP] and self.rect.y - self.vel > 0:
            self.rect.y -= self.vel
        if keys[pygame.K_DOWN] and self.rect.y + self.vel + self.height < RES[1]:
            self.rect.y += self.vel


def debug(surf, clock, font):
    txtFPS = font.render(str(int(clock.get_fps())), 1, WHITE)
    surf.blit(txtFPS, (RES[0]-txtFPS.get_width(), 0))


def main():
    run = True
    win = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()
    myFont = pygame.font.SysFont("Comic Sans MS", TAM//2)
    
    ball = Ball()
    enemy = Enemy()
    player = Player()
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: run = False
        
        keys = pygame.key.get_pressed()
        player.move(keys)
        enemy.move(keys)
        ball.move(player)
        ball.collide(player, enemy)
        
        win.fill(BLACK)
        debug(win, clock, myFont)
        ball.draw(win, player, myFont)
        enemy.draw(win)
        player.draw(win)
        
    
        pygame.display.update()
        clock.tick(FPS)
        
main()