import pygame
from random import randint, choice

GRAYBLUE = (6, 29, 31)
PURPLE = (248, 170, 255)

FPS = 60
TAM = 32
RES = (TAM*15, TAM*20)

class rainDrop():
  def __init__(self, rainDrops):
    self.x = randint(-TAM*3, RES[0])
    self.y = randint((-TAM * 5), 0)
    self.width = 1
    self.height = TAM
    self.vel = randint(0, 2)
    self.hspd = choice((-1, 1))
    self.vspd = 0
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    rainDrops.append(self)
  

  def draw(self, surf):
    pygame.draw.rect(surf, PURPLE, self.rect)


  def move(self, rainDrops):
    self.y += 20
    self.x += self.hspd * self.vel

    self.rect.y = self.y
    self.rect.x = self.x
    
    if self.rect.y > RES[1]:
      rainDrops.remove(self)

  

    
def rainManager(rainDrops, surf):
  for drop in rainDrops:
    drop.move(rainDrops)
    drop.draw(surf)

def main():
  run = True
  win = pygame.display.set_mode(RES)
  clock = pygame.time.Clock()
  count = 0
  rainMul = randint(3, 6)
  rainDrops = []


  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
  
    win.fill(GRAYBLUE)
    rainManager(rainDrops, win)

    if count <= 0:
      if rainMul - .1 > 0:
        n = randint(1, 5)
        while n > 0:
          rainDrop(rainDrops)
          n -= 1
      else:
          rainDrop(rainDrops)
      count = randint(0, (int(60*rainMul)))

      if rainMul - .1 > 0:
        rainMul -= .1
    elif count > 0:
      count -= 1
    print(count)
    pygame.display.update()
    clock.tick(FPS)

main()
