from pygame import *
from random import randint
from time import time as timer
mixer.init()
font.init()

x = 700
y = 500
window = display.set_mode((x,y))
display.set_caption('Шутер')
background = transform.scale(image.load('background.png'),(x,y))

mixer.music.load('space.ogg')
#mixer.music.play()
kick = mixer.Sound('space.ogg')


class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,w,h):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bulletboss1.png',self.rect.centerx,self.rect.top,-15,15,20)
        bullets.add(bullet)



lost = 0
kills = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > y:
            self.rect.y = 0
            self.rect.x = randint(50, 650)
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > y:
            self.rect.y = 0
            self.rect.x = randint(50,650)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()


ship = Player('player.png',350,400,10,50,50)

    
enemys1 = sprite.Group()
enemys2 = sprite.Group()
enemys3 = sprite.Group()

meteors = sprite.Group()

for _ in range(3):
    enemy1 = Enemy('enemy2_1.png',randint(50, 650),-40,randint(1, 5),65,65)
    enemy2 = Enemy('enemy2_2.png',randint(50, 650),-40,randint(1, 5),65,65)
    enemy3 = Enemy('boss3.png',randint(50, 650),-40,randint(1, 5),75,80)
    enemys1.add(enemy1)
    enemys2.add(enemy2)
    enemys3.add(enemy3)

meteor = Asteroid('meteor_3.png',randint(50, 650),-40,randint(1, 5),80,70)
meteors.add(meteor)

font1 = font.SysFont('comicsansms', 30)
font2 = font.SysFont('ebrima', 70)
finish = False
game = True
num_fire = 0
rel_time = False
while game:
    
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    ship.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    start_time = timer()
                    rel_time = True
                    
                
    if finish != True:
        
        window.blit(background,(0,0))
        missed = font1.render(f'Пропущено {lost}', True, (30,144,255))
        killed = font1.render(f'Убито {kills}', True, (255,69,0))
        win = font2.render(F'Победа', True, (0,128,0))
        lose = font2.render(f'Проигрыш',True, (255,0,0))
        window.blit(missed,(50,30))
        window.blit(killed,(50,70))
        ship.reset()
        ship.update()

        enemys1.draw(window)
        enemys2.draw(window)
        enemys3.draw(window)
        bullets.draw(window)
        meteors.draw(window)

        
        enemys1.update()
        enemys2.update()
        enemys3.update()
        bullets.update()
        display.update()
        meteors.update()

        if rel_time == True:
            end_time = timer()
            if end_time - start_time < 3:
                reload_time = font1.render(f'Подождите перезарядки...',True, (127,255,0))
                window.blit(reload_time,(100,150))
            else: 
                num_fire = 0
                rel_time = False


        sprites_list1 = sprite.groupcollide(enemys1,bullets,True,True)
        sprites_list2 = sprite.groupcollide(enemys2,bullets,True,True)
        sprites_list3 = sprite.groupcollide(enemys3,bullets,True,True)

        for _ in sprites_list1:
            kills += 1
            enemy1 = Enemy('enemy2_1.png',randint(50, 650),-40,randint(1, 5),65,65)
            enemys1.add(enemy1)
        for _ in sprites_list2:
            kills += 1
            enemy2 = Enemy('enemy2_2.png',randint(50, 650),-40,randint(1, 5),65,65)
            enemys2.add(enemy2)
        for _ in sprites_list3:
            kills += 1
            enemy3 = Enemy('boss3.png',randint(50, 650),-40,randint(1, 5),75,80)
            enemys3.add(enemy3)

        if kills == 50:
            finish = True
            window.blit(win,(300,200))
        
        if lost == 25:
            finish = True
            window.blit(lose,(300,200))
        display.update()
        

    time.delay(50)
