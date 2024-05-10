import pygame, sys
from player import Player
import obstcle
from alien import Alien,Extra
from random import choice,randint
from laser import Laser
class Game:

    #player setup
    def __init__(self):
        player_sprite=Player((screen_width/2,screen_height),screen_width,5)
        self.player=pygame.sprite.GroupSingle(player_sprite)
    #obstcle setup
        self.shape=obstcle.shape
        self.block_size=6
        self.blocks=pygame.sprite.Group()
        self.obstacle_amount=4
        self.obstacle_x_postions=[num *(screen_width /self.obstacle_amount) for num in range (self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_postions,x_start=screen_width/15,y_start=480)
     
    #Alien setup
        self.aliens=pygame.sprite.Group()
        self.alien_setup(rows=6,cols=8) 
        self.alien_direction=1
        self.alien_lasers=pygame.sprite.Group()
    #Extra setup
        self.extra=pygame.sprite.GroupSingle()
        self.extra_spawn_time=randint(40,80)
    #health and score setting
        self.lives=3
        self.live_surf=pygame.image.load('shooting game\graphics\player.png').convert_alpha()
        self.live_x_start_pos=screen_width -(self.live_surf.get_size()[0]*2+20)
        self.score=0
        self.font= pygame.font.Font('shooting game\Pixeled.ttf',20)
    #import all audio
        music=pygame.mixer.Sound('shooting game\Audio\music.wav')     
        music.set_volume(0.3) 
        music.play(loops=-1)
        self.laser_sound=pygame.mixer.Sound('shooting game\Audio\laser.wav')
        self.laser_sound.set_volume(0.4)
        self.explosion_sound=pygame.mixer.Sound('shooting game\Audio\explosion.wav')
        self.explosion_sound.set_volume(0.3)
        
        
       
    
    def create_obstacle(self,x_start,y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == 'x':
                    x = x_start+col_index * self.block_size + offset_x
                    y = y_start+ row_index * self.block_size
                    block = obstcle.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)
    def create_multiple_obstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
           self.create_obstacle(x_start,y_start,offset_x)
        
    def alien_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 100):            
        for row_index,row in enumerate(range(rows)):
            for col_index,col in enumerate(range(cols)):
                x= col_index * x_distance + x_offset
                y= row_index*x_distance+y_offset
                if row_index == 0: alien_sprite = Alien('\yellow',x,y)
                elif 1 <= row_index <= 2: alien_sprite = Alien('\green',x,y)
                else:alien_sprite=Alien('\Red',x,y)
                self.aliens.add(alien_sprite)
    def alien_postion_checker(self):
        all_aliens=self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right>=screen_width:
                self.alien_direction=-1
                self.alien_move_down(2)
            if alien.rect.left<=0:
                self.alien_direction=1
                self.alien_move_down(2)
    def alien_move_down(self,distance):
        if self.aliens:
         for alien in self.aliens.sprites():
              alien.rect.y+=distance
              
    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien=choice(self.aliens.sprites())
            laser_sprite=Laser(random_alien.rect.center,7,screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()    
    def extra_alien_time(self):
        self.extra_spawn_time -=1
        if self.extra_spawn_time<=0:
            self.extra.add(Extra(choice(['right','left']),screen_width))
            self.extra_spawn_time = randint(40,80)
     
    def collisions_checks(self):
        #player_lasers
        if self.player.sprite.lasers:    
            for lasers in self.player.sprite.lasers: 
                    #obstacle
                    if pygame.sprite.spritecollide(lasers,self.blocks,True):
                        lasers.kill()
                    #aliens
                    aliens_hit=pygame.sprite.spritecollide(lasers,self.aliens,True)
                    if aliens_hit:
                        for aliens in aliens_hit:
                            self.score+=aliens.value
                        lasers.kill()
                        self.explosion_sound.play()
                    if pygame.sprite.spritecollide(lasers,self.aliens,True):
                        lasers.kill()
                    #extra
                    if pygame.sprite.spritecollide(lasers,self.extra,True):
                        lasers.kill()
                        self.score+=500
    #alien-lasers
        if self.alien_lasers:    
            for lasers in self.alien_lasers:  
                #obstacle
                    if pygame.sprite.spritecollide(lasers,self.blocks,True):
                         lasers.kill()  
                #player
                    if pygame.sprite.spritecollide(lasers,self.player,False):
                
                        lasers.kill()  
                        self.lives-=1
                        if self.lives<=0:
                            pygame.quit()
                            sys.exit()
        
        
     #aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)
                if pygame.sprite.spritecollide(alien,self.player,False):
                    pygame.quit()
                    sys.exit()
     
    def display_lives(self):
        for live in range(self.lives-1):
            x=self.live_x_start_pos+(live*(self.live_surf.get_size()[0]+10))
            screen.blit(self.live_surf,(x,7))
    def display_score(self): 
        score_surf=self.font.render(f'score: {self.score}',False,'white')    
        score_rect=score_surf.get_rect(topleft=(10,-10))
        screen.blit(score_surf,score_rect)        
    def victory_message(self):
        if  not self.aliens.sprites():
              victory_surf=self.font.render('YOU WIN',False,"green")
              victory_rect=victory_surf.get_rect(center=(screen_width/2,screen_height/2))
              screen.blit(victory_surf,victory_rect)            
            
    def run(self):
        #updates
        self.player.update()
        self.extra.update()
        self.aliens.update(self.alien_direction)
        self.alien_lasers.update()
        #time
        self.extra_alien_time()
        #checker
        self.alien_postion_checker()
        self.collisions_checks()
        #screen/draw
        self.player.draw(screen)
        self.player.sprite.lasers.draw(screen)
        self.blocks.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.aliens.draw(screen)
        #display
        self.display_lives()
        self.display_score()
        #victory message
        self.victory_message()
        
       
       #update all sprite grop
       #draw all sprite groups
    
   
class CRT:
      def __init__(self):
         self.tv=pygame.image.load('shooting game\graphics\Tv.png').convert_alpha() 
         self.tv=pygame.transform.scale(self.tv,(screen_width,screen_height)) 
      def create_crt_lines(self):
          line_height=3
          line_amount=int(screen_height/line_height)
          for line in range(line_amount):
              y_pos=line*line_height
              pygame.draw.line(self.tv,'black',(0,y_pos),(screen_width,y_pos),1)
      def draw(self):
          self.tv.set_alpha(randint(69,90))
          self.create_crt_lines()
          screen.blit(self.tv,(0,0))
        
if __name__=='__main__':
    pygame.init()
    screen_width=600
    screen_height=600
    screen=pygame.display.set_mode((screen_width,screen_height))
    clock=pygame.time.Clock()
    game=Game()
    crt=CRT()
    
    ALIENLASER=pygame.USEREVENT+1
    pygame.time.set_timer(ALIENLASER,800)

    while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
         if event.type==ALIENLASER:
             game.alien_shoot()
      screen.fill((30,30,30))
      game.run()
      crt.draw()
    
      pygame.display.flip()
      clock.tick(60)
    
    
    