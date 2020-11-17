import pygame
import sys
import random

class Snake(object):
  def __init__(self):
    self.length = 1
    self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
    self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    self.color = (244, 81, 30)
    self.score = 0
    self.highScore = 0

  def get_head_position(self):
    return self.positions[0]
  
  def turn(self, point):
    if (self.length > 1) and ((point[0] * -1, point[1] * -1) == self.direction):
      return
    else:
      self.direction = point

  def move(self):
    cur = self.get_head_position()
    x, y = self.direction
    new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
    if (len(self.positions) > 2) and (new in self.positions[2:]):
      if self.score > self.highScore:
        self.highScore = self.score
      self.reset()
    else:
      self.positions.insert(0, new)
      if len(self.positions) > self.length:
        self.positions.pop()

  def reset(self):
    self.length = 1
    self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
    self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    self.score = 0

  def draw(self, surface):
    for p in self.positions:
      r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
      pygame.draw.rect(surface, self.color, r)
      pygame.draw.rect(surface, (250, 250, 250), r, 1) # border

  def handle_keys(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          self.turn(UP)
        elif event.key == pygame.K_DOWN:
          self.turn(DOWN)
        elif event.key == pygame.K_LEFT:
          self.turn(LEFT)
        elif event.key == pygame.K_RIGHT:
          self.turn(RIGHT)


class Food(object):
  def __init__(self):
    self.position = (0, 0)
    self.color = (25, 118, 210)
    self.randomize_position()
  
  def randomize_position(self):
    self.position = ((random.randint(0, GRID_WIDTH - 1) * GRIDSIZE), (random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE))
  
  def draw(self, surface):
    r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
    pygame.draw.rect(surface, self.color, r)
    pygame.draw.rect(surface, (25, 118, 210), r, 1) # border


def drawGrid(surface):
  for y in range(0, int(GRID_HEIGHT)):
    for x in range(0, int(GRID_WIDTH)):
      if (x + y) % 2 == 0:
        r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, (192, 202, 51), r)
      else:
        rr = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, (175, 180, 43), rr)


# GLOBAL VAR
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
  pygame.init()
  pygame.display.set_caption('Ular-ularan')

  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

  surface = pygame.Surface(screen.get_size())
  surface = surface.convert()

  snake = Snake()
  food = Food()

  myfont = pygame.font.Font('04B_19__.TTF', 20)

  # Geme Loop
  while(True):
    clock.tick(10)
    snake.handle_keys()
    drawGrid(surface)
    snake.move()
    if snake.get_head_position() == food.position:
      snake.length += 1
      snake.score += 1
      food.randomize_position() 
    snake.draw(surface)
    food.draw(surface)
    screen.blit(surface, (0, 0))  
    text_score = myfont.render("Score {0}".format(snake.score), 1, (255, 255, 255))
    text_highScore = myfont.render('High score {0}'.format(snake.highScore), 1, (255, 255, 255))
    screen.blit(text_score, (5, 10))
    screen.blit(text_highScore, (340, 10))
    pygame.display.update()

main()