#imports
import pygame
import random

#import keys
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

screen_width = 800
screen_height = 500

#the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load("granny.png")
        self.surf = pygame.transform.scale(self.surf, (150,120)).convert()
        self.surf.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect()
    
    #move sprite based on user pressed_keys
    def update(self,pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            # move_up_sound.play
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            # move_down_sound.play
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)    

        #keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height    

#the enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.surf = pygame.image.load("bottle.png")
        self.surf = pygame.transform.scale(self.surf, (20,20)).convert()
        self.surf.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width+20,screen_width+100),
                random.randint(0,screen_height)
                )
            )
        self.speed = random.randint(0,5)

    #remove enemy when passes left edge of screen
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()

#the trash
class Trash(pygame.sprite.Sprite):
    def __init__(self):
        super(Trash,self).__init__()
        self.surf = pygame.image.load("trash.png")
        self.surf = pygame.transform.scale(self.surf, (30,80)).convert()
        self.surf.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width+20,screen_width+100),
                random.randint(0,screen_height)
                )
            )
        self.speed = random.randint(0,5)

    #remove enemy when passes left edge of screen
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()

#game environment item
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud,self).__init__()
        self.surf = pygame.image.load("cloud.png")
        self.surf = pygame.transform.scale(self.surf, (100,50)).convert()
        self.surf.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(screen_width+20,screen_width+100),
                random.randint(0,screen_height)
            )
        )

    #move environment at constant speed
    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.right <0:
            self.kill()

#music
pygame.mixer.init()

#initialize
pygame.init()

#clock
clock = pygame.time.Clock()

#create screen
screen = pygame.display.set_mode((screen_width,screen_height))

#adding new enemy
ADDENEMY = pygame.USEREVENT +1
pygame.time.set_timer(ADDENEMY,500)

ADDCLOUD = pygame.USEREVENT +2
pygame.time.set_timer(ADDCLOUD,1000)

ADDTRASH = pygame.USEREVENT +3
pygame.time.set_timer(ADDTRASH,1000)

#initialize player
player = Player()

#separate sprite groups
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
trash = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#scoreboard font
font = pygame.font.SysFont('Helvetica', 18)

#music
# pygame.mixer.music.load("sound/Sky_dodge_theme.ogg")
# pygame.mixer.music.play(loops=-1)
# pygame.mixer.music.set_volume(0.1)

#local sounds
# move_up_sound = pygame.mixer.Sound("sound/jet_up.ogg")
# move_down_sound = pygame.mixer.Sound("sound/jet_down.ogg")
# collision_sound = pygame.mixer.Sound("sound/Boom.ogg")

#sound volumes
# move_up_sound.set_volume(0.6)
# move_down_sound.set_volume(0.6)
# collision_sound.set_volume(1.0)

#main loop
running = True
score = 0

while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        #add new cloud
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        #add new enemy
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        #add new trash
        elif event.type == ADDTRASH:
            new_trash = Trash()
            trash.add(new_trash)
            all_sprites.add(new_trash)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the enemy position abd clouds
    clouds.update()
    enemies.update()
    trash.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Update player sprite based on user keypresses
    player.update(pressed_keys)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()

        # Stop the loop
        running = False

    # Check if any trash have collided with the player
    elif pygame.sprite.spritecollideany(player, trash):
        # If so, add points
        score += 1    
        # Kill trash collided with
        pygame.sprite.spritecollideany(player, trash).kill()

        # Stop any moving sounds and play the collision
        # move_up_sound.stop()
        # move_down_sound.stop()
        # pygame.mixer.music.stop()
        # pygame.time.delay(50)
        # collision_sound.play()
        # pygame.time.delay(500)

    # Draw all clouds
    for entity in clouds:
        screen.blit(entity.surf, entity.rect)

    # Draw all enemies
    for entity in enemies:
        screen.blit(entity.surf, entity.rect)

    # Draw all trash
    for entity in trash:
        screen.blit(entity.surf, entity.rect)

    # Draw player
    screen.blit(player.surf, player.rect)

    # Display score
    scoreText = font.render("Score: " + str(score), 1, (0,0,0))
    screen.blit(scoreText, (20, 20))

    # Update the display
    pygame.display.flip()

    # Ensure the program maintains a maximum rate of 30 fps
    clock.tick(30)

# All done! Stop and quit the mixer
pygame.mixer.quit()
