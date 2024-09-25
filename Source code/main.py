
import pygame
from sprites import *
from config import *
import sys
import csv

class Game:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        #pygame.display.set_mode เปิดwindowของเกมตาม width height ที่หน่วยเป็น pixel โดย WIN_WIDTH WIN_HEIGHT def อยู่ไฟล์ Config
        self.clock=pygame.time.Clock()
        #pygame.time.clock() ใช่ set framerate
        self.pagefont = pygame.font.Font('fonts/arial.ttf',32)#the number is size of the font
        #pygame.font.Font
        self.scorefont = pygame.font.Font('fonts/ChakraPetch-Regular.ttf',16)
        self.running = True
        self.health = 10
        self.atk_damage = 1
        self.melee_damage = 2
        self.damage = 2
        self.add_score = 1
        self.score = 0
        self.orbnum = 0
        self.orb_time = 0

        self.defaultx = 6
        self.defaulty = 10

        self.timehit = 0
        self.timer = 0

        self.cooldown = 0
        #self.running is just a boolean that we will use when we want to stop playing the game
        self.character_spritesheet = Spritesheet('img/sprite.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemies_spritesheet = Spritesheet('img/sizedenemy.png')
        self.bosses_spritesheet = Spritesheet('img/bosses.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.fireball_spritesheet = Spritesheet('img/fireball.png')
        self.intro_background = pygame.image.load('img/sizedintro.png')
        self.go_background = pygame.image.load('img/gameover.png')
        self.explosion_spritesheet = Spritesheet('img/explosion.png')
        self.fireslide_spritesheet = Spritesheet('img/fireslide.png')
        self.enemyball_spritesheet = Spritesheet('img/Enemy_fireball.png')
        self.healingorb_spritesheet = Spritesheet('img/healingorb.png')
        self.yelloworb_spritesheet = Spritesheet('img/yelloworb.png')
        self.redorb_spritesheet = Spritesheet('img/redorb.png')
        self.title_spritesheet = Spritesheet('img/UnTitledExE.png')

        self.fireball_sound = pygame.mixer.Sound('sound/firesound.wav')
        self.fireball_sound.set_volume(0.1)
        self.swing_sound = pygame.mixer.Sound('sound/woosh.wav')
        self.swing_sound.set_volume(0.1)
        self.collide_sound = pygame.mixer.Sound('sound/collided.wav')
        self.collide_sound.set_volume(0.2)
        self.bg_music = pygame.mixer.music.load('sound/bgmusic.mp3')
        pygame.mixer.music.set_volume(0.1)

        
        self.score_list:list = []
        self.temp_score:list = []
        self.text = ''

        self.score_list.clear()
        self.text = ''
        self.score = 0
        leader = open("leaderboard.txt","r")
        c = csv.reader(leader,delimiter = ';',skipinitialspace=True)
        for line in c:
            if len(line) > 0:
                self.temp_score =scoreData(line)
                insert_at = len(self.score_list)
                for n in range(len(self.score_list)):
                    if self.temp_score.score > self.score_list[n].score:
                        insert_at = n
                        break
                self.score_list.insert(insert_at,self.temp_score)
        leader.close()
    
    def createTilemap(self):
        for i, row in enumerate(tilemap):#enumerateจะทำให้ได้ข้อมูลและตำแหน่งของ item (i is going to be posiont,row is going to be the Value or บรรทัด ขอว string)
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column == "B":
                    Block(self,j,i)
                if column == "P":
                    self.player = Player(self,j,i)#ใน sprite.py มีclass Player(self(คือตัวclassเองเราไม่ต้องสนใจ),game,x,y) ดังนั้นเราจึงใส่ (self(ในที่นี้หมายถึงตัวClass Game เพราะเราอยู่ในfile main.py),1,2)
                if column == "E":
                    Enemy(self,j,i,self.player)
                if column == "V":
                    Boss(self,j,i)
                if column == "W":
                    Fireslide(self,j,i)

    def new(self):
        self.playing = True
        #this is gonna be call whenever we run our game it gonna set apart all varieble for our game
        #a new game start
        #will be useful when we want to see if our player die or not or quit game
        self.all_sprites = pygame.sprite.LayeredUpdates()#Object ที่เก็บ sprite ทั้งหมดที่เราใช่ในเกม note การที่เก็บไว้ในกลุ่มเดียวกันทำให้update ได้ทีเดียวเลย
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.rangeattacks = pygame.sprite.LayeredUpdates()
        self.meleeattacks = pygame.sprite.LayeredUpdates()
        self.bosses = pygame.sprite.LayeredUpdates()
        self.enemies_atk = pygame.sprite.LayeredUpdates()
        self.player_sprites = pygame.sprite.LayeredUpdates()
        self.orb = pygame.sprite.LayeredUpdates()
        
        self.createTilemap()
        #class เป็นblueprint ของ object
        

    def events(self):
        #game loop events
        for event in pygame.event.get():
            #pygame.event.get is going to get every event that happen in pygame and we going to iterate over that list
            if event.type==pygame.QUIT:
                #pygame.quit จะเช็คว่าเรากดปุ่มปิด(กากะบาด)หรือป่าว
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self,self.player.rect.x-8,self.player.rect.y-TILESIZE)
                        self.swing_sound.play()
                    if self.player.facing == 'down':
                        Attack(self,self.player.rect.x-8,self.player.rect.y+(TILESIZE/2))
                        self.swing_sound.play()
                    if self.player.facing == 'left':
                        Attack(self,self.player.rect.x-TILESIZE,self.player.rect.y)
                        self.swing_sound.play()
                    if self.player.facing == 'right':
                        Attack(self,self.player.rect.x+(TILESIZE/2),self.player.rect.y)
                        self.swing_sound.play()

                if event.key == pygame.K_z:
                    if pygame.time.get_ticks() - self.cooldown >= 150:
                        if self.player.facing == 'up':
                            Fireball(self,self.player.rect.x-8,self.player.rect.y)
                            self.fireball_sound.play()
                        if self.player.facing == 'down':
                            Fireball(self,self.player.rect.x-8,self.player.rect.y)
                            self.fireball_sound.play()
                        if self.player.facing == 'left':
                            Fireball(self,self.player.rect.x,self.player.rect.y-8)
                            self.fireball_sound.play()
                        if self.player.facing == 'right':
                            Fireball(self,self.player.rect.x,self.player.rect.y-8)
                            self.fireball_sound.play()
                        self.cooldown = pygame.time.get_ticks()

                if event.type == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False

    def update(self):
        #game loop updates
        self.timer = pygame.time.get_ticks()
        self.all_sprites.update()
        #self.all.sprites is that sprite group that we have this layered update(Line 22-26) which is a object that contain method called update
        #which gonna find update method in every single sprites thats in that group and run update method that is in Sprite.py

    def draw(self):
        #game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        #.draw method look through every sprite find image find rectangle and draw it on windowI(in this case sprite and rectangle is in Sprite.py)
        self.clock.tick(FPS)
        self.scoredisplay()
        pygame.display.update()

    def main(self):
        #game loop
        pygame.mixer.music.play(-1)
        while self.playing:
            self.events()#events method(func) gonna contain everything like keypress event
            self.update()#Update the game to make sure it isnt a static image
            self.draw()#draw sprites
        pygame.mixer.music.stop()

    def game_over(self):
        gameOver=self.pagefont.render('Game Over',True,WHITE)
        gameOver_rect = gameOver.get_rect(x=230,y=150)
        continue_button = Button(230,210,160,50,WHITE,BLACK,'CONTINUE',32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if continue_button.is_pressed(mouse_pos,mouse_pressed):
                self.new()
                self.main()
                self.health = 10

            self.screen.blit(self.go_background,(0,0))
            self.screen.blit(gameOver,gameOver_rect) #display text at text_rect
            self.screen.blit(continue_button.image,continue_button.rect)#display button at button rect
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True
        self.timer = 0
        title=self.title_spritesheet.get_sprite(0,0,435,54)
        title.set_colorkey(BLACK)
        title_rect = title.get_rect(x=100,y=90)#input is Title Rect position
        play_button = Button(270,210,100,50,WHITE,BLACK,'PLAY',32)
        stat_button = Button(270,325,100,50,WHITE,BLACK,'STAT',32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()#get mouse position
            mouse_pressed = pygame.mouse.get_pressed()#check if mouse button is pressed

            if play_button.is_pressed(mouse_pos,mouse_pressed) :
                intro = False#when intro is False the loop is broken then the program can moveon to the g.new
            if stat_button.is_pressed(mouse_pos,mouse_pressed) :
                intro = False
                self.statistic()

            self.screen.blit(self.intro_background,(0,0))
            self.screen.blit(title,title_rect) 
            self.screen.blit(play_button.image,play_button.rect) #display play_button.image to play_button.rect
            self.screen.blit(stat_button.image,stat_button.rect) 
            self.namedisplay()
            self.clock.tick(FPS)
            pygame.display.update()
        

    def statistic(self):
        stat = True
        self.timer = 0
        self.ypos =120
        back=self.pagefont.render('Statistic',True,WHITE)
        back_rect = back.get_rect(x=260,y=50)#input is Title Rect position
        self.score_list.clear()
        self.text = ''
        self.score = 0
        leader = open("leaderboard.txt","r")
        c = csv.reader(leader,delimiter = ';',skipinitialspace=True)
        for line in c:
            if len(line) > 0:
                self.temp_score =scoreData(line)
                insert_at = len(self.score_list)
                for n in range(len(self.score_list)):
                    if self.temp_score.score > self.score_list[n].score:
                        insert_at = n
                        break
                self.score_list.insert(insert_at,self.temp_score)
        leader.close()
        return_button = Button(270,400,100,50,WHITE,BLACK,'Return',32)

        self.screen.blit(self.intro_background,(0,0))
        self.screen.blit(back,back_rect) 
        self.screen.blit(return_button.image,return_button.rect) #display play_button.image to play_button.rect
        for i in range(len(self.score_list)):# up to 5 highscore names and scores
            name_list = self.scorefont.render(f"{self.score_list[i].get_score_data('display')}",True,WHITE)
            name_rect = name_list.get_rect(x = 270,y = self.ypos)
            self.screen.blit(name_list,name_rect)
            self.ypos += 30

        while stat:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            mouse_pos = pygame.mouse.get_pos()#get mouse position
            mouse_pressed = pygame.mouse.get_pressed()#check if mouse button is pressed

            if return_button.is_pressed(mouse_pos,mouse_pressed) : 
                stat = False#when intro is False the loop is broken then the program can moveon to the g.new
                self.intro_screen()

            
            self.clock.tick(FPS)
            pygame.display.update()


    def scoredisplay(self):
        scoretext = self.scorefont.render('Health = %d Score = %d'%(self.health,self.score),True,WHITE)
        scoretext_rect = scoretext.get_rect(x=450,y=20)
        self.screen.blit(scoretext,scoretext_rect)

    def namedisplay(self):
        scoretext = self.scorefont.render('Phonphat Chintathum 65010700',True,WHITE)
        scoretext_rect = scoretext.get_rect(x=400,y=20)
        self.screen.blit(scoretext,scoretext_rect)

    def writename(self):
        self.iwidth = 200
        self.iheight = 50
        self.bwidth = 204
        self.bheight = 54

        #game over text
        gameOver=self.pagefont.render('!Finished!',True,WHITE)
        gameOver_rect = gameOver.get_rect(x=260,y=100)

        #button
        continue_button = Button(238,300,180,50,WHITE,BLACK,'CONTINUE',32)

        #input box
        color_inactive = RED
        color_active = WHITE
        color = color_inactive
        self.input_box = pygame.Surface((self.iwidth,self.iheight))
        self.input_box.fill(BLACK)
        self.input_rect = self.input_box.get_rect()
        self.input_rect.x = 230
        self.input_rect.y = 200
        self.border = pygame.Surface((self.bwidth,self.bheight))
        self.border.fill(color)
        self.border_rect = self.border.get_rect()
        self.border_rect.x = 228
        self.border_rect.y = 198
        active = False

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_pressed = pygame.mouse.get_pressed()

            if continue_button.is_pressed(self.mouse_pos,self.mouse_pressed) and len(self.text) > 0:
                self.temp_score = scoreData((self.text,self.score))
                insert_at = len(self.score_list)
                for n in range(len(self.score_list)):
                    if self.temp_score.score > self.score_list[n].score:
                        insert_at = n
                        break
                self.score_list.insert(insert_at,self.temp_score)

                lines = 0
                leader = open("leaderboard.txt","w")
                for i in range(len(self.score_list)):
                    if lines < 5:
                        leader.write(self.score_list[i].get_score_data("file"))
                    lines += 1
                leader.close()
                self.health = 10
                self.score = 0
                self.intro_screen()
                self.new()
                self.main()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if self.input_rect.collidepoint(self.mouse_pos):
                        # Toggle the active variable.
                        active = True
                        color = color_active if active else color_inactive
                        self.border.fill(color)
                    else:
                        active = False
                        color = color_active if active else color_inactive
                        self.border.fill(color)
                    # Change the current color of the input box.
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            
                        if event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]

                        elif len(self.text)<=15:
                            self.text += event.unicode

            self.screen.blit(self.go_background,(0,0))
            self.screen.blit(gameOver,gameOver_rect) #display text at text_rect
            self.screen.blit(continue_button.image,continue_button.rect)#
            self.txt_surface = self.scorefont.render(self.text, True, WHITE)
            self.screen.blit(self.border,self.border_rect)
            self.screen.blit(self.input_box,self.input_rect)
            self.screen.blit(self.txt_surface,(240,210))
            # Blit the input_box rect.
            self.clock.tick(FPS)
            pygame.display.update()
            
class scoreData():
    def __init__(self, line:list):
        self.name = line[0]
        self.score = int(line[1])

    def get_score_data(self,dest:str) -> str:
        if dest == 'file':
            return f"{self.name} ; {self.score} \n"
        else:
            return f"{self.name} : {self.score}"


g=Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.writename()
    #g.game_over()

pygame.quit()
sys.exit()