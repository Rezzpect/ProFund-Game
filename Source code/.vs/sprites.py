
import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha() #convert() will help load image alot faster and wont make our game slow down

    def get_sprite(self,x,y,width,height): #will cut out the sprite sheet
        sprite = pygame.Surface([width,height])#create a surface
        sprite.blit(self.sheet,(0,0),(x,y,width,height)) #(0,0)is to place top right of the sheet at (0,0) of the surface then place the image on surface ,Note x y will be the starting point of the crop while width and height determent the size of the crop regtangle
        sprite.set_colorkey(BLACK)#this make color ()in the image transparent
        return sprite

class Player(pygame.sprite.Sprite):
    #Class python modle that make it easier to make sprites This mean our Player is now a sprites
    #Note : pygame.sprite.Sprite is a inherited class
    
    def __init__(self,game,x,y): #x y to set where player appear on the screen
        #by passing in game we can access all the variable in Game(class) from main file
        self.game=game
        self._layer=PLAYER_LAYER
        # notice pygame.sprite.LayeredUpdates() from main file, by setting the layer we can tell pygame in what layer
        #we want the sprite to appear also PLAYER_LAYER need to be def as num in config file
        self.groups=self.game.all_sprites,self.game.player_sprites
        #by setting self.group we basically set player sprite to all sprite group, We can add Play to all sprite group because we going to passe Game in here as a Object.read next code
        pygame.sprite.Sprite.__init__(self,self.groups)
        #call the init method for inherited class and by passing in the group we adding player to all sprite group
        self.x=x * TILESIZE
        self.y=y * TILESIZE
        self.width=15
        self.height=18

        self.rOrb_stat = False
        self.red_duration = 7000
        self.red_pickup = 0
        self.red_interval = 0
        self.yOrb_stat = False
        self.yellow_duration = 3000
        self.yellow_pickup = 0
        self.heal_interval = 0

        self.x_change = 0
        self.y_change = 0
        #these are temporary variables that will store the change in movement during one loop.

        self.facing = 'right'
        self.oldfacing = 'right'
        #self.facing doesnt have any impact on the game at the moment but it will once we start to use animations!
        
        self.animation_loop=1
        self.image = self.game.character_spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect=self.image.get_rect()#set Rectangle(Rect) size
        #Rect is like a hitbox
        self.rect.x=self.x
        self.rect.y=self.y
        #set Rectangle position

    def redcheck(self):
        if self.rOrb_stat == True:
            if pygame.time.get_ticks() - self.red_pickup <= self.red_duration:
                if (pygame.time.get_ticks() - self.heal_interval > 1000) and self.game.health > 1:
                    self.game.health -= 1
                    self.heal_interval = pygame.time.get_ticks()
                self.game.atk_damage = 3
                self.game.melee_damage = 9
                self.game.add_score = 3
            else:
                self.rOrb_stat = False
                self.game.damage = 1
                self.game.melee_damage = 3
                self.game.add_score = 1
                if self.red_duration > 7000:
                    self.red_duration = 7000
                

    def yellowcheck(self):
        if self.yOrb_stat == True:
            if pygame.time.get_ticks() - self.yellow_pickup <= self.yellow_duration:
                if pygame.time.get_ticks() - self.heal_interval > 1000:
                    self.game.health += 1
                    self.heal_interval = pygame.time.get_ticks()
            else:
                self.yOrb_stat = False
                if self.yellow_duration > 3000:
                    self.yellow_duration = 3000
    def update(self):
    #every pygame sprite has to have a method call update
        self.movement()
        self.animate()
        self.collide_enemy()
        self.redcheck()
        self.yellowcheck()

        if self.game.health <= 0:
            self.kill()
            self.game.playing = False

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.x_change -= PLAYER_SPEED
            self.facing = 'left'
            self.oldfacing = 'left'
        if keys[pygame.K_RIGHT]:
            if self.rect.x < 620:
                self.x_change += PLAYER_SPEED
            self.facing = 'right'
            self.oldfacing = 'right'
        if keys[pygame.K_UP]:
            if self.rect.y > 0:
                self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            if self.rect.y < 462:
                self.y_change += PLAYER_SPEED
            self.facing = 'down'
        #���ͧ�ҡ� pygame 㹢ͺ˹�Ҩͺ��ش�դ�� y=0 ��Ш������������� ����͹���ŧ �������ش����� y=480���������褹���

    def collide_blocks(self,direction):
        if direction == "x":
            hits=pygame.sprite.spritecollide(self,self.game.blocks,False)#this will check whether rect of one sprite is colliding with rect of the another sprite in this case we use it in player class which mean we looking at player sprite and we comparing it block sprite
            #the third parameter of the function will check if we want to delete the sprite when collide or not
            #hit=return 0 not hit = return 1
            if hits:
                if self.x_change>0:
                    self.rect.x = hits[0].rect.left - self.rect.width#hit.[0].rect.left will put our Player rect on the top left of the rec on it[0] which is the wall we collide with then - self.rect.width which will move player back =width
                if self.x_change<0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits=pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.y_change>0:
                    self.rect.y = hits[0].rect.top - self.rect.height #same as rect.left
                if self.y_change<0:
                    self.rect.y = hits[0].rect.bottom
        
    def collide_enemy(self):
        boss_hits = pygame.sprite.spritecollide(self,self.game.enemies,False)
        if boss_hits:
            if (self.game.timer - self.game.timehit) > 1000:
               self.game.collide_sound.play()
               self.game.health -= 1
               self.game.timehit = self.game.timer
               #if (pygame.time.get_ticks() - self.timehit) <= 1000:
     

    def animate(self):
        rightidle_animations = [self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(16, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(48, 0, self.width, self.height)]

        leftidle_animations = [self.game.character_spritesheet.get_sprite(0, 46, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(16, 46, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(32, 46, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(48, 46, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(0, 23, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(16, 23, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 23, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(48, 23, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(0, 69, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(16, 69, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(32, 69, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(48, 69, self.width, self.height)]
        if self.facing =="down":
            if self.y_change == 0 and self.oldfacing == 'left':
                self.image=leftidle_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
            elif self.y_change == 0 and self.oldfacing == 'right':
                self.image=rightidle_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
            elif self.oldfacing == 'left':
                self.image=left_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
            elif self.oldfacing == 'right':
                self.image=right_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1

        if self.facing =="up":
            if self.y_change == 0 and self.oldfacing == 'left':
                self.image=leftidle_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
            elif self.y_change == 0 and self.oldfacing == 'right':
                self.image=rightidle_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
            elif self.oldfacing == 'left':
                self.image=left_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
            elif self.oldfacing == 'right':
                self.image=right_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1

        if self.facing =="left":
            if self.x_change == 0:
                self.image=leftidle_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
            else:
                self.image=left_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1

        if self.facing =="right":
            if self.x_change == 0:
                self.image=rightidle_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
            else:
                self.image=right_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self,game,x,y,player):
         
        self.player = player
        self.game = game
        self._layer=ENEMY_LAYER
        self.groups = self.game.all_sprites,self.game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width= TILESIZE
        self.height= TILESIZE
        self.attackedcd = 0
        self.health = 3

        self.x_change = 0
        self.y_change = 0
        
        self.facing = 'right'

        self.image = self.game.enemies_spritesheet.get_sprite(0,0,self.width,self.height)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def get_distance_direct(self):
        play_vec = pygame.math.Vector2(self.player.rect.center)
        enemy_vec = pygame.math.Vector2(self.rect.center)
        distance = (play_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (play_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)

    def update(self):
        self.movement()
        self.animate()
        self.loot_drop()
        self.collide_atk()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        self.x_change=0
        self.y_change=0

    def loot_drop(self):
        if self.health <= 0:
            drop = random.randrange(1,12)
            if drop == 1:
                YellowOrb(self.game,self.rect.x,self.rect.y)
            if drop == 2:
                RedOrb(self.game,self.rect.x,self.rect.y)
            if drop == 3:
                HealingOrb(self.game,self.rect.x,self.rect.y)
            self.game.score += self.game.add_score*2
            self.kill()

    def collide_atk(self):
        rangeatk_hit = pygame.sprite.spritecollide(self,self.game.rangeattacks,True)
        if rangeatk_hit:
            self.health -= self.game.atk_damage

        meleeatk_hit = pygame.sprite.spritecollide(self,self.game.meleeattacks,False)
        if meleeatk_hit and pygame.time.get_ticks() - self.attackedcd >= 500:
            self.health -= self.game.melee_damage
            self.attackedcd = pygame.time.get_ticks()

    def collide_blocks(self,direction):
        if direction == "x":
            hits=pygame.sprite.spritecollide(self,self.game.blocks,False)#this will check whether rect of one sprite is colliding with rect of the another sprite in this case we use it in player class which mean we looking at player sprite and we comparing it block sprite
            #the third parameter of the function will check if we want to delete the sprite when collide or not
            #hit=return 0 not hit = return 1
            if hits:
                if self.x_change>0:
                    self.rect.x = hits[0].rect.left - self.rect.width#hit.[0].rect.left will put our Player rect on the top left of the rec on it[0] which is the wall we collide with then - self.rect.width which will move player back =width
                   
                if self.x_change<0:
                    self.rect.x = hits[0].rect.right
        if direction == "y":
            hits=pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.y_change>0:
                    self.rect.y = hits[0].rect.top - self.rect.height #same as rect.left
                   
                if self.y_change<0:
                    self.rect.y = hits[0].rect.bottom
                   
    
    def movement(self):
        if self.player.rect.x >= self.rect.x:
            self.facing = 'right'
        else:
            self.facing = 'left'

        self.distance = self.get_distance_direct()[0]
        self.direction = self.get_distance_direct()[1]
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.x_change += self.direction.x * ENEMY_SPEED
        self.y_change += self.direction.y * ENEMY_SPEED

    def animate(self):
        left_animations = [self.game.enemies_spritesheet.get_sprite(0, 0, self.width, self.height)]

        right_animations = [self.game.enemies_spritesheet.get_sprite(0, 32, self.width, self.height)]
        
        if self.facing =="left":
            self.image = left_animations[0]

        if self.facing =="right":
            self.image = right_animations[0]

class Block(pygame.sprite.Sprite):
    def __init__(self,game,x,y):

        self.game=game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960,448 ,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x =x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE
        self.list = [32*12,32*13,32*14]
        self.pos = random.choice(self.list)

        self.image = self.game.terrain_spritesheet.get_sprite(self.pos,160,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Button:
    def __init__(self,x,y,width,height,fg,bg,content,fontsize):
        self.font = pygame.font.Font('fonts/arial.ttf',fontsize)
        self.content = content

        self.x=x
        self.y=y
        self.width=width
        self.height=height

        self.fg=fg 
        self.bg=bg 

        self.image =pygame.Surface((self.width,self.height))
        self.image.fill(self.bg)
        self.rect=self.image.get_rect()

        self.rect.x = self.x 
        self.rect.y=self.y
        self.text = self.font.render(self.content,True,self.fg)#the middle is put is anti alias
        self.text_rect=self.text.get_rect(center=(self.width/2,self.height/2)) #text_rect is position of the text ,center is going put text in middle of the button
        self.image.blit(self.text,self.text_rect) #put text into the image
#get position of mouse check if it collide and check if we click or not
    def is_pressed(self,pos,pressed): 
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):

    def __init__(self,game,x,y):

        self.game=game 
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites,self.game.meleeattacks
        pygame.sprite.Sprite.__init__(self,self.groups) 

        self.x = x
        self.y = y 
        self.width = TILESIZE 
        self.height = TILESIZE 
        
        self.animation_loop=0
        self.direction =self.game.player.facing

        self.image = self.game.attack_spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self,self.game.enemies,False)#True will delete kill the enermy when collide

    def animate(self):

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        if self.direction =='up':
            self.image=up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 #one attack sprite stay for 2 frame
            if self.animation_loop >= 5:
                self.kill()

        if self.direction =='down':
            self.image=down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 #one attack sprite stay for 2 frame
            if self.animation_loop >= 5:
                self.kill()

        if self.direction =='left':
            self.image=left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 #one attack sprite stay for 2 frame
            if self.animation_loop >= 5:
                self.kill()

        if self.direction =='right':
            self.image=right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 #one attack sprite stay for 2 frame
            if self.animation_loop >= 5:
                self.kill()

class Fireball(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game 
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites,self.game.rangeattacks
        pygame.sprite.Sprite.__init__(self,self.groups) 

        self.x = x
        self.y = y
        self.original_x = self.x
        self.original_y = self.y
        self.width = TILESIZE 
        self.height = TILESIZE 
        self.x_change = 0
        self.y_change = 0
        self.direction = self.game.player.facing
        
        self.animation_loop=0
        self.image = self.game.fireball_spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

    def update(self):
        self.animate()
        self.collide()

        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x_change = 0
        self.y_change = 0

    def collide(self):
        hits = pygame.sprite.spritecollide(self,self.game.enemies,False)#True will delete kill the enermy when collide
        block_hits = pygame.sprite.spritecollide(self,self.game.blocks,False,pygame.sprite.collide_rect_ratio(0.5))
        if block_hits:
            self.kill()

    def animate(self):

        left_animations = [self.game.fireball_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.fireball_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.fireball_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.fireball_spritesheet.get_sprite(96, 64, self.width, self.height)]

        down_animations = [self.game.fireball_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.fireball_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.fireball_spritesheet.get_sprite(64, 0, self.width, self.height),
                           self.game.fireball_spritesheet.get_sprite(96, 0, self.width, self.height)]

        right_animations = [self.game.fireball_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.fireball_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.fireball_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.fireball_spritesheet.get_sprite(96, 96, self.width, self.height)]

        up_animations = [self.game.fireball_spritesheet.get_sprite(0, 32, self.width, self.height),
                         self.game.fireball_spritesheet.get_sprite(32, 32, self.width, self.height),
                         self.game.fireball_spritesheet.get_sprite(64, 32, self.width, self.height),
                         self.game.fireball_spritesheet.get_sprite(96, 32, self.width, self.height)]

        if self.direction =='up':
            self.image=up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 #one attack sprite stay for 2 frame
            self.y_change -= BALL_SPEED
            if(self.original_y - self.rect.y >= 200):
                self.kill()
            if self.animation_loop >= 4:
                self.animation_loop = 0

        if self.direction =='down':
            self.image=down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 #one attack sprite stay for 2 frame
            if self.animation_loop >= 4:
                self.animation_loop = 0
            self.y_change += BALL_SPEED
            if(self.rect.y - self.original_y >= 200):
                self.kill()

        if self.direction =='left':
            self.image=left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 #one attack sprite stay for 2 frame
            if self.animation_loop >= 4:
                self.animation_loop = 0
            self.x_change -= BALL_SPEED
            if(self.original_x - self.rect.x >= 200):
                self.kill()

        if self.direction =='right':
            self.image=right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 #one attack sprite stay for 2 frame
            if self.animation_loop >= 4:
                self.animation_loop = 0
            self.x_change += BALL_SPEED
            if(self.rect.x - self.original_x >= 200):
                self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
         
        self.game = game
        self._layer=ENEMY_LAYER
        self.groups = self.game.all_sprites,self.game.bosses,self.game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.randatk = 0
        self.attackedcd = 0
        self.wait_start = pygame.time.get_ticks()
        self.sincestart = pygame.time.get_ticks()
        self.atk_start = 0
        self.atk_duration = 15000
        self.wait_duration = 7000
        self.atk_range = 4
        self.attackedcd = 0
        self.enemy_num = 5
        self.enemy_spawn = False
        self.facing = 'left'

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.start = True
        self.blink = 128
        self.slide = 1
        self.limit = 0
        self.limit_swap = 19
        self.direction = 2
        
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width= TILESIZE
        self.height= TILESIZE

        self.atkend = True
        self.x_change = 0
        self.y_change = 0
        self.cooldown = 0
        
        '''self.facing = random.choice(['left','right'])
        self.animation_loop=1
        self.movement_loop=0
        self.max_travel = random.randint(7,30)'''

        self.image = self.game.bosses_spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def animate(self):
        if self.game.player.rect.x >= self.rect.x:
            self.facing = 'right'
        else:
            self.facing = 'left'

        left_animations = [self.game.bosses_spritesheet.get_sprite(0, 0, self.width, self.height)]

        right_animations = [self.game.bosses_spritesheet.get_sprite(32, 0, self.width, self.height)]
        
        if self.facing =="left":
            self.image = left_animations[0]

        if self.facing =="right":
            self.image = right_animations[0]

    def update(self):
        self.collide()
        self.animate()
        if self.start == True:
            Enemy(self.game,-1,-1,self.game.player)
            Enemy(self.game,-1,15,self.game.player)
            Enemy(self.game,20,-1,self.game.player)
            Enemy(self.game,20,15,self.game.player)
            self.start = False

        #difficulty scaling
        if pygame.time.get_ticks() - self.sincestart >= 60000:
            self.game.damage += 2
            self.wait_duration -= 1000
            if self.enemy_num <= 8:
                self.enemy_num += 1
            if self.atk_range < 10:
                self.atk_range +=2
            self.sincestart = pygame.time.get_ticks()
        
        #after atk(rand new atk)
        if (pygame.time.get_ticks() - self.wait_start <= self.wait_duration): 
            if self.atkend == True:
                 if self.enemy_spawn == True:
                        Enemy(self.game,-1,-1,self.game.player)
                        Enemy(self.game,-1,15,self.game.player)
                        Enemy(self.game,20,-1,self.game.player)
                        Enemy(self.game,20,15,self.game.player)
                         #enemy_spawn_x *= -1
                 self.enemy_spawn = False
                #self.game.score += 1

        if (pygame.time.get_ticks() - self.wait_start > self.wait_duration) :
            if self.atkend == True:
                #self.game.score += 1
                Enemy(self.game,-1,-1,self.game.player)
                Enemy(self.game,-1,15,self.game.player)
                Enemy(self.game,20,-1,self.game.player)
                Enemy(self.game,20,15,self.game.player)
                self.newlo_x = random.randrange(0,20)
                self.newlo_y = random.randrange(0,15)
                while self.newlo_x == 3 or self.newlo_x == 4 or self.newlo_x == 5 or self.newlo_x == 14 or self.newlo_x == 15 or self.newlo_x == 16:
                    if self.newlo_y == 3 or self.newlo_y == 4 or self.newlo_y == 5 or self.newlo_y == 9 or self.newlo_y == 10 or self.newlo_y == 11:
                        self.newlo_x = random.randrange(0,20)
                        self.rect.y = random.randrange(0,15)
                    else:
                        break
                self.rect.x = self.newlo_x * TILESIZE
                self.rect.y = self.newlo_y * TILESIZE
                self.randatk = random.randrange(1,self.atk_range)
                self.atk_start = pygame.time.get_ticks()
                self.atkend = False

        #while atk
        if pygame.time.get_ticks() - self.atk_start <= self.atk_duration:
            if self.atkend == False: 
                if self.randatk == 1:
                    self.explosion_attack()
                if self.randatk == 2:
                    self.slide_attack()
                if self.randatk == 3:
                    self.ball_atk_LRC()
                if self.randatk == 4:
                    self.ball_atk_LR()
                if self.randatk == 5:
                    self.explosion_attack()
                    self.slide_attack()
                if self.randatk == 6:
                    self.blink_explosion()
                if self.randatk == 7:
                    self.ball_atk_LRRB()
                if self.randatk == 8:
                    self.ball_atk_UC()
                if self.randatk == 9:
                    self.ball_atk_URB()
                #self.game.score += 1

        if pygame.time.get_ticks() - self.atk_start > self.atk_duration: 
            if self.atkend == False:
                self.newlo_x = random.randrange(0,20)
                self.newlo_y = random.randrange(0,15)
                while self.newlo_x == 3 or self.newlo_x == 4 or self.newlo_x == 5 or self.newlo_x == 14 or self.newlo_x == 15 or self.newlo_x == 16:
                    if self.newlo_y == 3 or self.newlo_y == 4 or self.newlo_y == 5 or self.newlo_y == 9 or self.newlo_y == 10 or self.newlo_y == 11:
                        self.newlo_x = random.randrange(0,20)
                        self.rect.y = random.randrange(0,15)
                    else:
                        break
                self.rect.x = self.newlo_x * TILESIZE
                self.rect.y = self.newlo_y * TILESIZE
                self.atkend = True
                self.enemy_spawn = True
                self.wait_start = pygame.time.get_ticks()
                self.game.score += 1
                
        
    def collide(self):
        range_hit = pygame.sprite.spritecollide(self,self.game.rangeattacks,True)
        melee_hit = pygame.sprite.spritecollide(self,self.game.meleeattacks,False)
        if(range_hit):
            self.game.score += self.game.add_score
        if melee_hit and pygame.time.get_ticks() - self.attackedcd >= 500:
            self.game.score += self.game.add_score * 3
            self.attackedcd = pygame.time.get_ticks()

    def explosion_attack(self):
        self.lo_x = random.randrange(0,21)
        self.lo_y = random.randrange(0,16)
        if pygame.time.get_ticks() - self.cooldown > 50:
            warning(self.game,self.lo_x,self.lo_y)
            Explosion(self.game,self.lo_x,self.lo_y)
            self.cooldown = pygame.time.get_ticks()

    def slide_attack(self):
        self.lo_x = 0
        self.lo_y = random.randrange(0,16)
        if pygame.time.get_ticks() - self.cooldown > 400:
            if self.lo_x == 0:
                while self.lo_x <= 19:
                    warning(self.game,math.floor(self.lo_x),self.lo_y)    
                    Fireslide(self.game,math.floor(self.lo_x),self.lo_y)
                    self.lo_x += 1
                self.cooldown = pygame.time.get_ticks()

    def ball_atk_LR(self):
        if pygame.time.get_ticks() - self.cooldown > 2000:
            self.lo_x = 0
            self.lo_y = 0
            while self.lo_y < 15:
                warning(self.game,self.lo_x,self.lo_y)
                Enemyball(self.game,self.lo_x,self.lo_y,2,True) #from left
                self.lo_y += 2
            self.lo_x = 19
            self.lo_y = 15
            while self.lo_y > -1:
                warning(self.game,self.lo_x,self.lo_y)
                Enemyball(self.game,self.lo_x,self.lo_y,1,True) #from right
                self.lo_y -= 2
            self.cooldown = pygame.time.get_ticks()

    def ball_atk_LRC(self):
        if pygame.time.get_ticks() - self.cooldown > 700:
            temp_x = self.game.player.rect.x - self.blink
            if temp_x < 0:
                temp_x = 0
            if temp_x > 640:
                temp_x = 608
            temp_y = self.game.player.rect.y
            self.rect.x = temp_x
            self.rect.y = temp_y
            while pygame.sprite.spritecollide(self,self.game.blocks,False):
                self.rect.x += self.slide
            Enemyball(self.game,self.rect.x/32,self.rect.y/32,self.direction,False) #from left
            self.direction -= self.slide
            self.blink *= -1
            self.slide *= -1
            self.cooldown = pygame.time.get_ticks()

    def ball_atk_LRRB(self):
        if pygame.time.get_ticks() - self.cooldown > 4000:
            self.lo_y = 0
            self.blank = random.randrange(0,15)
            while self.lo_y <= 14:
                if self.lo_y != self.blank:
                    warning(self.game,0,self.lo_y)
                    Enemyball(self.game,0,self.lo_y,2,True) #from left
                    warning(self.game,19,self.lo_y)
                    Enemyball(self.game,19,self.lo_y,1,True) #from right
                self.lo_y += 1
            self.cooldown = pygame.time.get_ticks()
            
    def ball_atk_URB(self):
        if pygame.time.get_ticks() - self.cooldown > 3500:
            Enemy(self.game,-1,-1,self.game.player)
            Enemy(self.game,20,15,self.game.player)
            self.lo_y = 0
            self.lo_x = 0
            self.blank = random.randrange(0,20)
            while self.lo_x <= 19:
                if self.lo_x != self.blank:
                    warning(self.game,self.lo_x,self.lo_y)
                    Enemyball(self.game,self.lo_x,self.lo_y,0,True) #from above
                self.lo_x += 1
            self.cooldown = pygame.time.get_ticks()

    def ball_atk_UC(self):
        if pygame.time.get_ticks() - self.cooldown > 70:
            self.lo_x = random.randrange(0,20)
            self.lo_y = 0 
            warning(self.game,self.lo_x,self.lo_y)
            Enemyball(self.game,self.lo_x,self.lo_y,0,True) #from above
            self.cooldown = pygame.time.get_ticks()

    def blink_explosion(self):
        if pygame.time.get_ticks() - self.cooldown > 1500:
            listx = [(self.game.player.rect.x/32)-1,(self.game.player.rect.x/32)+1]
            self.newlo_x = random.choice(listx)
            self.newlo_y = self.game.player.rect.y/32
            self.rect.x = self.newlo_x * TILESIZE
            self.rect.y = self.newlo_y * TILESIZE
            if self.rect.x < 0:
                self.rect.x = 0
            if self.rect.x > 640:
                self.rect.x = 608
            if self.newlo_x == (self.game.player.rect.x/32)-1:
                while pygame.sprite.spritecollide(self,self.game.blocks,False):
                    self.rect.x += 32
            else:
                while pygame.sprite.spritecollide(self,self.game.blocks,False):
                    self.rect.x -= 32
            self.lo_x = self.rect.x/32 + 1
            self.lo_y = self.rect.y/32 
            warning(self.game,self.lo_x,self.lo_y)
            Explosion(self.game,self.lo_x,self.lo_y)
            Enemyball(self.game,self.lo_x,self.lo_y,2,True) #from left
            self.lo_y -= 1
            warning(self.game,self.lo_x,self.lo_y)
            Explosion(self.game,self.lo_x,self.lo_y) 
            self.lo_x -= 1
            warning(self.game,self.lo_x,self.lo_y)
            Explosion(self.game,self.lo_x,self.lo_y)
            Enemyball(self.game,self.lo_x,self.lo_y,3,True)
            self.lo_x -= 1
            warning(self.game,self.lo_x,self.lo_y)
            Explosion(self.game,self.lo_x,self.lo_y)
            self.lo_y += 1
            warning(self.game,self.lo_x,self.lo_y)
            Explosion(self.game,self.lo_x,self.lo_y)
            Enemyball(self.game,self.lo_x,self.lo_y,1,True)
            self.lo_y += 1
            warning(self.game,self.lo_x,self.lo_y)
            Explosion(self.game,self.lo_x,self.lo_y)
            self.lo_x +=1
            warning(self.game,self.lo_x,self.lo_y)
            Explosion(self.game,self.lo_x,self.lo_y)
            Enemyball(self.game,self.lo_x,self.lo_y,0,True)
            self.lo_x +=1
            warning(self.game,self.lo_x,self.lo_y)
            Explosion(self.game,self.lo_x,self.lo_y)
            self.cooldown = pygame.time.get_ticks()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer = EN_ATK_LAYER
        self.groups = self.game.all_sprites,self.game.enemies_atk
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE 
        self.height = TILESIZE 
        self.animation_loop = 0
        
        self.image = self.game.explosion_spritesheet.get_sprite(192,0,self.width,self.height).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.time = pygame.time.get_ticks()

    def animate(self):
            animation =[self.game.explosion_spritesheet.get_sprite(0,0,self.width,self.height),
                       self.game.explosion_spritesheet.get_sprite(32,0,self.width,self.height),
                       self.game.explosion_spritesheet.get_sprite(64,0,self.width,self.height),
                       self.game.explosion_spritesheet.get_sprite(96,0,self.width,self.height),
                       self.game.explosion_spritesheet.get_sprite(128,0,self.width,self.height),
                       self.game.explosion_spritesheet.get_sprite(160,0,self.width,self.height),]

            self.image=animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 5:
               self.kill()

    def update(self):
        if pygame.time.get_ticks() - self.time >= 1500:
            self.animate()
            self.collide_player()

    def collide_player(self):
        self.attack_hits = pygame.sprite.spritecollide(self,self.game.player_sprites,False,pygame.sprite.collide_rect_ratio(0.85))
        if self.attack_hits:
            if (self.game.timer - self.game.timehit) > 1000:
                self.game.collide_sound.play()
                self.game.health -= self.game.damage
                self.game.timehit = self.game.timer
               #if (pygame.time.get_ticks() - self.timehit) <= 1000:


class warning(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = WARN_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x =x*TILESIZE
        self.y =y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE
        self.timer = 0
        self.round = 0

        self.image = pygame.Surface((self.width,self.height)).convert_alpha()
        self.image.fill((255,0,0,100))
        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        self.time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.time >=1500:
            self.kill()
class Firewall(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer = EN_ATK_LAYER
        self.groups = self.game.all_sprites,self.game.enemies_atk
        pygame.sprite.Sprite.__init__(self,self.groups) 

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = 288
        self.height = 64
        self.animation_loop = 0
        
        self.image = self.game.firewall_spritesheet.get_sprite(0,388,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.time = pygame.time.get_ticks()

    def animate(self):
            animation =[self.game.firewall_spritesheet.get_sprite(0,0,self.width,self.height),
                       self.game.firewall_spritesheet.get_sprite(0,65,self.width,self.height),
                       self.game.firewall_spritesheet.get_sprite(0,129,self.width,self.height),
                       self.game.firewall_spritesheet.get_sprite(0,192,self.width,self.height),
                       self.game.firewall_spritesheet.get_sprite(0,256,self.width,self.height),
                       self.game.firewall_spritesheet.get_sprite(0,290,self.width,self.height),]

            self.image=animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 5:
               self.animation_loop=0

    def update(self):
        if pygame.time.get_ticks() - self.time >= 1500:
            self.animate()
            self.collide_player()

    def collide_player(self):
        self.attack_hits = pygame.sprite.spritecollide(self,self.game.player_sprites,False)
        if self.attack_hits:
            if (self.game.timer - self.game.timehit) > 1000:
                self.game.collide_sound.play()
                self.game.health -= self.game.damage
                self.game.timehit = self.game.timer
               #if (pygame.time.get_ticks() - self.timehit) <= 1000:

class Fireslide(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer = EN_ATK_LAYER
        self.groups = self.game.all_sprites,self.game.enemies_atk
        pygame.sprite.Sprite.__init__(self,self.groups) 

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.animation_loop = 0
        
        self.image = self.game.fireslide_spritesheet.get_sprite(64*6,0,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.time = pygame.time.get_ticks()

    def animate(self):
            animation =[self.game.fireslide_spritesheet.get_sprite(0,0,self.width,self.height),
                       self.game.fireslide_spritesheet.get_sprite(32,0,self.width,self.height),
                       self.game.fireslide_spritesheet.get_sprite(64,0,self.width,self.height),
                       self.game.fireslide_spritesheet.get_sprite(98,0,self.width,self.height),
                       self.game.fireslide_spritesheet.get_sprite(130,0,self.width,self.height),
                       self.game.fireslide_spritesheet.get_sprite(162,0,self.width,self.height),]

            self.image=animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 5:
               self.animation_loop=self.kill()

    def update(self):
        if pygame.time.get_ticks() - self.time >= 1500:
            self.animate()
            self.collide_player()

    def collide_player(self):
        self.attack_hits = pygame.sprite.spritecollide(self,self.game.player_sprites,False,pygame.sprite.collide_rect_ratio(0.85))
        if self.attack_hits:
            if (self.game.timer - self.game.timehit) > 1000:
                self.game.collide_sound.play()
                self.game.health -= self.game.damage
                self.game.timehit = self.game.timer
               #if (pygame.time.get_ticks() - self.timehit) <= 1000:

class Enemyball(pygame.sprite.Sprite):
    def __init__(self,game,x,y,direction,delay):
        self.game=game
        self._layer = EN_ATK_LAYER
        self.groups = self.game.all_sprites,self.game.enemies_atk
        pygame.sprite.Sprite.__init__(self,self.groups) 
        if delay == True:
            self.delay = 1500
        else:
            self.delay = 0
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.animation_loop = 0
        self.lo = [0,32,32*2,32*3]
        self.direction = direction
        self.select = self.lo[direction]
        self.time = 0
        self.ready = 0
        
        self.image = self.game.enemyball_spritesheet.get_sprite(0,32*4,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.time = pygame.time.get_ticks()

    def animate(self):
            animation =[self.game.enemyball_spritesheet.get_sprite(0,self.select,self.width,self.height),
                       self.game.enemyball_spritesheet.get_sprite(32,self.select,self.width,self.height),
                       self.game.enemyball_spritesheet.get_sprite(64,self.select,self.width,self.height),
                       self.game.enemyball_spritesheet.get_sprite(96,self.select,self.width,self.height)]

            self.image=animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 3:
               self.animation_loop = 0

            if self.direction == 0:
                if self.rect.y >= 480:
                    self.kill()

            if self.direction == 1:
                if self.rect.x <= 0:
                    self.kill()

            if self.direction == 2:
                if self.rect.x >= 640:
                    self.kill()

            if self.direction == 3:
                if self.rect.y <= 0:
                    self.kill()

    def collide_player(self):
        self.attack_hits = pygame.sprite.spritecollide(self,self.game.player_sprites,False,pygame.sprite.collide_rect_ratio(0.75))
        if self.attack_hits:
            if (self.game.timer - self.game.timehit) > 1000:
                self.game.collide_sound.play()
                self.game.health -= self.game.damage
                self.game.timehit = self.game.timer
               #if (pygame.time.get_ticks() - self.timehit) <= 1000:

    def update(self):
        if pygame.time.get_ticks() - self.time >= self.delay:
            self.animate()
            self.collide_player()
            self.ready = 1

        if self.ready == 1:
            if self.direction == 0:
                self.rect.y += 2

            if self.direction == 1:
                self.rect.x -= 2

            if self.direction == 2:
                self.rect.x += 2

            if self.direction == 3:
                self.rect.y -= 2

class HealingOrb(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites,self.game.orb
        pygame.sprite.Sprite.__init__(self,self.groups) 

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.droptime = pygame.time.get_ticks()
        
        self.image = self.game.healingorb_spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.time = pygame.time.get_ticks()

    def collide_player(self):
        self.orb_get = pygame.sprite.spritecollide(self,self.game.player_sprites,False,pygame.sprite.collide_rect_ratio(0.50))
        if self.orb_get:
            self.game.health += 3
            self.game.score += 50
            self.kill()
               #if (pygame.time.get_ticks() - self.timehit) <= 1000:

    def update(self):
        self.collide_player()
        if pygame.time.get_ticks() - self.droptime > 15000:
            self.kill()

class RedOrb(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites,self.game.orb
        pygame.sprite.Sprite.__init__(self,self.groups) 

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.droptime = pygame.time.get_ticks()
        
        self.image = self.game.redorb_spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.time = pygame.time.get_ticks()

    def collide_player(self):
        self.orb_get = pygame.sprite.spritecollide(self,self.game.player_sprites,False,pygame.sprite.collide_rect_ratio(0.50))
        if self.orb_get:
            if self.game.player.rOrb_stat == False:
                self.game.player.rOrb_stat = True
                self.game.player.red_pickup = pygame.time.get_ticks()
            else:
                self.game.player.red_duration += 2000
            self.kill()
               #if (pygame.time.get_ticks() - self.timehit) <= 1000:

    def update(self):
        self.collide_player()
        if pygame.time.get_ticks() - self.droptime > 15000:
            self.kill()
            
class YellowOrb(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites,self.game.orb
        pygame.sprite.Sprite.__init__(self,self.groups) 

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.droptime = pygame.time.get_ticks()
        self.image = self.game.yelloworb_spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.time = pygame.time.get_ticks()

    def collide_player(self):
        self.orb_get = pygame.sprite.spritecollide(self,self.game.player_sprites,False,pygame.sprite.collide_rect_ratio(0.50))
        if self.orb_get:
            if self.game.player.yOrb_stat == False:
                self.game.player.yOrb_stat = True 
                self.game.player.yellow_pickup = pygame.time.get_ticks()
                self.game.player.heal_interval = pygame.time.get_ticks()
                self.game.health += 1
            else:
                self.game.player.yellow_duration += 2000
            self.kill()
               #if (pygame.time.get_ticks() - self.timehit) <= 1000:

    def update(self):
        self.collide_player()
        if pygame.time.get_ticks() - self.droptime > 15000:
            self.kill()
            


        


