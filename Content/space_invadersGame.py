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

# Load win/loose/loose_health sound effect
win_sound = pygame.mixer.Sound("Music/win.mp3")
lose_sound = pygame.mixer.Sound("Music/lost.mp3")
health_sound = pygame.mixer.Sound("Music/lost_health.mp3")



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
            if player.health_remaining >= 10:  #to only play the sound unless the shoot is the game over scene
                health_sound.play()


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





# Define font and colors for text
font = pygame.font.Font(None, 36)
text_color = (255, 255, 255)

# Create text surfaces
you_won_text = font.render("You won !!", True, text_color)
game_over_text = font.render("Game Over", True, text_color)

# Create button rectangles
restart_button = pygame.Rect(300, 400, 200, 50)
quit_button = pygame.Rect(300, 500, 200, 50)




game = True
win_sound_played = False
lose_sound_played = False




# Main game loop
while game:

# Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over == 1 or game_over == 2:
                # Check if the mouse click is inside the restart or quit buttons
                if restart_button.collidepoint(event.pos):
                    # Reset the entire game
                    create_invaders()
                    player = Player(int(window_width / 2), window_height - 80)
                    player_group.empty()  # Clear player group
                    player_group.add(player)
                    playerBullet_group.empty()  # Clear player bullet group
                    invaderBullet_group.empty()  # Clear invader bullet group
                    player.health_remaining = player.health_start
                    timer = pygame.time.get_ticks()
                    game_over = 0
                    initial_state = True  # Set the game state to initial
                elif quit_button.collidepoint(event.pos):
                    game = False  # Quit the game


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
        if not win_sound_played:
            win_sound.play()  # Play the win sound
            win_sound_played = True
        # Create restart and quit buttons
        pygame.draw.rect(screen, (0, 0, 128), restart_button)
        pygame.draw.rect(screen, (0, 0, 128), quit_button)

        # Create text for buttons
        restart_text = font.render("Restart Game", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        # Center text on buttons
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)

        # Draw text on buttons
        screen.blit(restart_text, restart_text_rect)
        screen.blit(quit_text, quit_text_rect)

    elif game_over == 2:
        screen.blit(game_over_image, (0, 0))
        if not lose_sound_played:
            lose_sound.play()  # Play the lose sound
            lose_sound_played = True


        # Create restart and quit buttons
        pygame.draw.rect(screen, (0, 0, 128), restart_button)
        pygame.draw.rect(screen, (0, 0, 128), quit_button)

        # Create text for buttons
        restart_text = font.render("Restart Game", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        # Center text on buttons
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)

        # Draw text on buttons
        screen.blit(restart_text, restart_text_rect)
        screen.blit(quit_text, quit_text_rect)


    # Updates the content state of the screen
    pygame.display.update()

pygame.quit()     