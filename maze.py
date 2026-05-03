from pygame import *
from dataclasses import dataclass

init()
font.init()

mixer.music.load("jungles.ogg")
mixer.music.play() 
kick = mixer.Sound("kick.ogg")
money = mixer.Sound("money.ogg")

window = display.set_mode((700, 500))
display.set_caption("Лабанов")
background = transform.scale(image.load("background.jpg"), (1000, 500))

@dataclass
class Sprite:
    x: int
    y: int
    filename: str
    speed: int
    
    def __post_init__(self):
        self.img = transform.scale(image.load(self.filename), (50, 50))
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.direction = ("up")

    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))

    def update_p2(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5: self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 645: self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5: self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 445: self.rect.y += self.speed

    def monster_move(self, y_min, y_max):
        if self.rect.y <= y_min:
            self.direction = "down"

        elif self.rect.y >= y_max:
            self.direction = "up"

        if self.direction == "up":
            self.rect.y -= self.speed

        elif self.direction == "down":
            self.rect.y += self.speed


@dataclass
class Wall:
    color: tuple
    wall_x: int
    wall_y: int
    wall_width: int
    wall_height: int

    def __post_init__(self):
        self.rect = Rect(self.wall_x, self.wall_y, self.wall_width, self.wall_height)

    def draw_wall(self):
        draw.rect(window, self.color, self.rect)

GREEN = (0, 255, 0)
RED = (255, 0, 0)

w1 = Wall(GREEN, 100, 20, 420, 10)
w2 = Wall(GREEN, 100, 400, 420, 10)
w3 = Wall(GREEN, 100, 20, 10, 380)
w4 = Wall(GREEN, 510, 80, 10, 330)

final = Sprite(600, 200, "treasure.png", 0) 
hero1 = Sprite(200, 200, "hero.png", 5)
monster = Sprite(550, 300, "cyborg.png", 5)

clock = time.Clock()

game = True
finish = False

font = font.Font(None, 60)
lose_text = font.render(
    "you lose, try hard", True, (255,255,255)
)

win_text = font.render(
    "you win", True, (255, 255, 255)
)


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if not finish:
        window.blit(background, (0, 0))
        
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()

        hero1.update_p2()
        hero1.draw()
        monster.draw()
        monster.monster_move(20, 350)
        final.draw()

        if sprite.collide_rect(hero1, monster) or sprite.collide_rect(hero1, w1) or \
           sprite.collide_rect(hero1, w2) or sprite.collide_rect(hero1, w3):
            window.blit(lose_text, (200, 200))
            kick.play()
            finish = True
            time.delay(2000)
            game = False

        if sprite.collide_rect(hero1, final): 
            window.blit(win_text, (200, 200))
            money.play()
            finish = True
            time.delay(2000)
            game = False

    display.update()
    clock.tick(60)

quit()