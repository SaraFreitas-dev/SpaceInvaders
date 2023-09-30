import pygame
import random
import pygame.mixer

pygame.init()
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("Music/Crusher_Boss.mp3")
pygame.mixer.music.play(-1)  # Continuous playback

# Load shooting sound effect
shoot_sound = pygame.mixer.Sound("Music/shoot.mp3")
shoot_sound.set_volume(0.4) 

# Surface to draw the game
window_height = 600
window_width = 800
rows = 4
cols = 10
game_over = 0

clock = pygame.time.Clock()
timer = pygame.time.get_ticks()

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space Invaders")
background = pygame.image.load("Images/background.png")

# Sprite is a computer graphics term for any object on the screen that can move around
invaders_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
playerBullet_group = pygame.sprite.Group()
invaderBullet_group = pygame.sprite.Group()

# BULLETS (INVADERS/USER)

class player_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/user_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        # if it collides...
        if pygame.sprite.spritecollide(self, invaders_group, True):
            self.kill()


class invader_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/invader_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if pygame.sprite.spritecollide(self, player_group, False):
            self.kill()
            player.health_remaining -= 10


# Define the object and its type

class Invader(pygame.sprite.Sprite):
    # Coordinates of the Sprites
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/spaceInvaders.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_direction = 1
        self.move_counter = 0

    # Movement of the invaders
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1

        if self.move_counter > 75:
            self.move_direction *= -1
            self.move_counter *= -1


# Create the invaders and choose their position
def create_invaders():
    for row in range(rows):
        for col in range(cols):
            invader = Invader(100 + col * 65, 80 + row * 50)
            invaders_group.add(invader)


# Call the player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/user.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()  # keep track of the last time shot
        self.health_start = 50
        self.health_remaining = 50

    # KEY COMMANDS
    def update(self):
        speed = 2
        cooldown = 100
        current_time = pygame.time.get_ticks()
        key = pygame.key.get_pressed()
        gameover = 0

        # Draw health
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x, self.rect.bottom, self.rect.width, 10))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, (0, 255, 0),
                             (self.rect.x, self.rect.bottom, int(self.rect.width * (self.health_remaining / self.health_start)), 10))
            if self.health_remaining == 0:
                self.kill()
                gameover = 2

        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed

        if key[pygame.K_RIGHT] and self.rect.right < window_width:
            self.rect.x += speed

        if key[pygame.K_SPACE] and current_time - self.last_shot > cooldown:
            bullet = player_bullet(self.rect.centerx, self.rect.top)
            playerBullet_group.add(bullet)
            self.last_shot = pygame.time.get_ticks()
            # Play the shooting sound effect
            shoot_sound.play()

        return gameover


# Call the create_invaders() function to create the invaders and the same for the player and bullets
def create_invader_bullet():
    # Randomly select two different invaders
    if len(invaders_group) > 6:
        attacking_invaders = random.sample(invaders_group.sprites(), 3)
    
    if len(invaders_group) <= 6:
        # Randomly select two different invaders
        attacking_invaders = random.sample(invaders_group.sprites(), 1)

    for attacking_invader in attacking_invaders:
        invaderBullet = invader_bullet(attacking_invader.rect.centerx, attacking_invader.rect.centery)
        invaderBullet_group.add(invaderBullet)

create_invaders()
player = Player(int(window_width/2), window_height - 80)
player_group.add(player)



game = True


# Main game loop
while game:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    # Speed of invaders movement
    clock.tick(60)
    screen.blit(background, (0, 0))

    if len(invaders_group) == 0:
        game_over = 1

    if player.health_remaining == 0:
        game_over = 2    
     

    if game_over == 0:
        # Time between each invader attack bullet
        seconds = (pygame.time.get_ticks() - timer) / 1000
        if (seconds > 2):
            create_invader_bullet()
            timer = pygame.time.get_ticks()

        invaders_group.update()
        player_group.update()
        invaderBullet_group.update()
        playerBullet_group.update()

        invaders_group.draw(screen)
        player_group.draw(screen)
        invaderBullet_group.draw(screen)
        playerBullet_group.draw(screen)
        game_over = player.update()

    game_over_image = pygame.image.load("Images/gameover.png")
    win_image = pygame.image.load("Images/win.jpg")
    game_over_image = pygame.transform.scale(game_over_image, (window_width, window_height))
    win_image = pygame.transform.scale(win_image, (window_width, window_height))
    
    if game_over == 1:
        screen.blit(win_image, (0, 0))
    elif game_over == 2:
        screen.blit(game_over_image, (0, 0))

    # Updates the content state of the screen
    pygame.display.update()

pygame.quit()     