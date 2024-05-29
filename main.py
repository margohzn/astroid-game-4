import pygame
import random
import math 

pygame.init()

screen_width = 800 
screen_height = 800 
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Hit the astroid game!")


clock = pygame.time.Clock()

# loading images
bg_img = pygame.image.load("images/starbg.png")
alien_img = pygame.image.load("images/alienShip.png")
player_rocket = pygame.image.load("images/spaceRocket.png")
star_img = pygame.image.load("images/star.png")
asteroid50 = pygame.image.load("images/asteroid50.png")
asteroid100 = pygame.image.load("images/asteroid100.png")
asteroid150 = pygame.image.load("images/asteroid150.png")

# loading sound
shoot_sound = pygame.mixer.Sound("sound/shoot.wav")
bangSmall_sound = pygame.mixer.Sound("sound/bangSmall.wav")
bangLarge_sound = pygame.mixer.Sound("sound/bangLarge.wav")

shoot_sound.set_volume(0.25)
bangSmall_sound.set_volume(0.25)
bangLarge_sound.set_volume(0.25)


game_over = False
lives = 5 
score = 0 
rapid_fire = False # cannot press fire button non stop
rf_start = -1
is_sound_on = True 
count =0 
high_score = 0
run = True


player_bullets = []
asteroids = []
stars = []
aliens = []
alien_bullets = [] 

class Player(object):
    def __init__(self):
        self.img = player_rocket
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = screen_width // 2
        self.y = screen_height // 2 
        self.angle = 0 
        self.rotated_surface = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect()
        self.rotated_rect.center = (self.x,self.y)
        self.cosin = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosin * self.width // 2, self.y - self.sine * self.height // 2)

    def draw(self, screen):
        screen.blit(self.rotated_surface, self.rotated_rect)

    def turn_left(self):
        self.angle += 5 
        self.rotated_surface = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect()
        self.rotated_rect.center = (self.x,self.y)
        self.cosin = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosin * self.width // 2, self.y - self.sine * self.height // 2)

    def turn_right(self):
        self.angle -= 5 
        self.rotated_surface = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect()
        self.rotated_rect.center = (self.x,self.y)
        self.cosin = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosin * self.width // 2, self.y - self.sine * self.height // 2)

    def move_farward(self):
        self.x += self.cosin * 6
        self.y -= self.sine * 6
        self.rotated_surface = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect()
        self.rotated_rect.center = (self.x,self.y)
        self.cosin = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosin * self.width // 2, self.y - self.sine * self.height // 2)

    def update_location(self):
        if self.x > screen_width + 50:
            self.x = 0 
        elif self.x < 0 - self.width:
            self.x = screen_width
        elif self.y > screen_height + 50:
            self.y = 0
        elif self.y < -50:
            self.y = screen_height
    


class Bullets(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.width, self.height = 4,4
        self.c = player.cosin
        self.s = player.sine
        self.vx = self.c * 10 
        self.vy = self.c * 10 

    def move(self):
        self.x += self.vx 
        self.y -= self.vy 

    def draw():
        pygame.draw.rect(screen, (255,255,255), [self.x, self.y, self.width, self.height])

    def check_offscreen(self):
        if self.x < -50 or self.x > screen_width or self.y < -50 or self.y > screen_height:
            return True 
        
class Astroids(object):
    def __init__(self, rank):
        self.rank = rank 
        if self.rank == 1:
            self.image = asteroid50
        elif self.rank == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        self.width = 50 * rank 
        self.height = 50 * rank 
        self.rand_point = random.choice([(random.randrange(0,screen_width - self.width), random.choice([-1 * self.height - 5, self.height + 5])), (random.choice([-1 * self.width -5, screen_width + 5]), random.randrange(0,screen_height - self.height))])
        self.x, self.y = self.rand_point
        if self.x < screen_width // 2:
            self.xdir = 1 
        else:
            self.xdir = -1

        if self.y < screen_height // 2:
            self.ydir = 1 
        else:
            self.ydir = -1

        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1,3)

    def draw(self, screen):
        screen.blit(self.image, self.x,self.y)

    
class Star(object):
    def __init__(self):
        self.image = star_img 
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rand_point = random.choice([(random.randrange(0,screen_width - self.width), random.choice([-1 * self.height - 5, self.height + 5])), (random.choice([-1 * self.width -5, screen_width + 5]), random.randrange(0,screen_height - self.height))])
        self.x, self.y = self.rand_point
        if self.x < screen_width:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < screen_height:
            self.ydir = 1 
        else:
            self.ydir = -1 

        self.vx = self.x * random.randrange(1,3)
        self.vy = self.y * random.randrange(1,3)

    def draw(self, screen):
        screen.blit(self.image, self.x,self.y)



class Alien(object):
    def __init__(self):
        self.image = alien_img 
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rand_point = random.choice([(random.randrange(0,screen_width - self.width), random.choice([-1 * self.height - 5, self.height + 5])), (random.choice([-1 * self.width -5, screen_width + 5]), random.randrange(0,screen_height - self.height))])
        self.x, self.y = self.rand_point
        if self.x < screen_width:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < screen_height:
            self.ydir = 1 
        else:
            self.ydir = -1 

        self.vx = self.x * random.randrange(1,3)
        self.vy = self.y * random.randrange(1,3)

    def draw(self, screen):
        screen.blit(self.image, self.x,self.y)


class AlienBullet(object):
    def __init__(self, x,y):
        self.x = x 
        self.y = y 
        self.width = 4
        self.height = 4 
        self.dirx, self.diry = player.x - self.x, player.y - self.y 
        self.dist = math.hypot(self.dirx, self.diry)
        self.dx, self.dy = self.dirx/self.dist, self.diry/self.dist
        self.xv = self.dx * 5
        self.vy = self.dy * 5 

    def draw(self, screen):
        pygame.draw.rect(screen, "pink", [self.x,self.y,self.width,self.height])


def redraw_game_window():
    screen.blit(bg_img, (0,0))
    font = pygame.font.SysFont("arial", 30)
    lives_text = font.render("Lives: " + str(lives), 1, (255,255,255))
    play_again_text = font.render("Press tab to play again", 1, (255,255,255))
    score_text = font.render("Score: " + str(score), 1, (255,255,255))
    high_score_text = font.render("High Score: " + str(high_score), 1, (255,255,255))

    player.draw(screen)

    for a in asteroids:
        a.draw(screen)

    for b in player_bullets:
        b.draw(screen)

    for s in stars:
        s.draw(screen)

    for i in aliens:
        i.draw(screen)

    for b in alien_bullets:
        b.draw(screen)

    if rapid_fire:
        pygame.draw.rect(screen, (0,0,0), [screen_width // 2 - 51 ,19,102,22])
        pygame.draw.rect(screen, (255,255,255), [screen_width //2 - 50, 20, 100 - 100 *(count-rf_start) / 500, 20])

    if game_over:
        screen.blit(play_again_text, (screen_width//2 - play_again_text.get_width() // 2, screen_height//2 - play_again_text.get_height()//2))

    screen.blit(lives_text, (25,25))
    screen.blit(score_text, (screen_width//2 - score_text.get_width() -25,  25))
    screen.blit(high_score_text, (screen_width - high_score_text.get_width()- 25, 35 + score_text.get_height))
    pygame.display.update()


player = Player()

while run:
    clock.tick(60)
    count += 1 

    if not game_over:
        if asteroids 