import pygame
import random
import math

# initializing pygame
pygame.init()

# -- CREATE WINDOW --
# -- full screen
# ecran = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

# -- reduce screen
ecran = pygame.display.set_mode((500, 500))
x_screen, y_screen= ecran.get_size()
pygame.display.set_caption("Space Invader exercice")

# -- INITIALIZATION --
# background
background = pygame.image.load('images/background.jpg')
background = pygame.transform.scale(surface=background, size=(x_screen, y_screen))

# Score
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('fonts/VT323-Regular.ttf', 20)

# Game Over
game_over_font = pygame.font.Font('fonts/VT323-Regular.ttf', 64)


def show_score(x, y):
	score = font.render("Score: " + str(score_val),
						True, (255,255,255))
	ecran.blit(score, (x, y))

def game_over():
	game_over_text = game_over_font.render("GAME OVER",
										True, (255,255,255))
	ecran.blit(game_over_text, (190, 250))

# player
player = pygame.image.load('images/spaceship.png')
player = pygame.transform.scale(surface=player, size=(50, 50))
player_rect = player.get_rect()
x_player= x_screen/2
y_player = y_screen-100

# invader
invaders_images = []
x_invader = []
y_invader = []
x_invader_direction = []
y_invader_direction = []
nb_of_invaders = 4

def invader(x, y, i):
	ecran.blit(invaders_images[i], (x, y))
    
def collision(x1, x2, y1, y2):
	distance = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2)))
	if distance <= 30:
		return True
	else:
		return False
        
for num in range(nb_of_invaders):
    invaders_images.append(pygame.image.load('images/invader.png'))
    x_invader.append(random.randint(0, x_screen))
    y_invader.append(random.randint(0, y_screen/2))
    x_invader_direction.append(random.choice([-2.5, 2.5]))
    y_invader_direction.append(50)

# missile
missile = pygame.image.load('images/missile.png').convert_alpha()
missile = pygame.transform.scale(surface=missile, size=(30, 30))

#missilepos = missileobj(0,y_screen-150)
x_missile = 0
y_missile = y_screen-150
x_missile_speed = 0
y_missile_speed = 6
is_fire = False

def fire_bullet(x, y):
    # Chercher le booléen
    global is_fire
    is_fire = True
    ecran.blit(missile, (x, y))


# -- LOOP --
loop = True
while loop:
    # pygame event

    # Sert à ne pas avoir de répétitions
    # ecran.fill((0,0,0))
    ecran.blit(background, (0,0))

    for event in pygame.event.get():
        # event input clavier
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loop = False
            if event.type == pygame.QUIT:
                loop = False
            if event.key == pygame.K_SPACE:
                if is_fire == False:
                    x_missile = x_player
                    fire_bullet(x_missile, y_player)
    
    # Pour que le joueur puisse se déplacer en laissant la touche appuyée
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        # bordure à gauche
        if x_player>0:
            x_player-=5
        else:
            x_player=0
    if pressed[pygame.K_RIGHT]:
        # bordure à droite
        # On met x_screen-50 car l'image a une taille de 50x50
        if x_player<x_screen-50:
            x_player+=5
        else:
            x_player=x_screen-50

    # Mouvements de l'invader
    for i in range(nb_of_invaders):
        x_invader[i]+=x_invader_direction[i]

        if y_invader[i] >= 450:
            if abs(x_player-x_invader[i]) < 80:
                for j in range(nb_of_invaders):
                    y_invader[j] = 2000
                    game_over()
                    break

        if x_invader[i] >= x_screen-50 or x_invader[i] <= 0:
            x_invader_direction[i] *= -1
            y_invader[i] += y_invader_direction[i]

        kill = collision(x_missile, x_invader[i], y_missile, y_invader[i])
		
        if kill:
            score_val += 1
            y_missile = y_screen-130
            is_fire = False
            x_invader[i] = 2000
            y_invader[i] = 130
            x_invader_direction[i] *= -1
        
        invader(x_invader[i], y_invader[i], i)

    if is_fire:
        fire_bullet(x_missile, y_missile)
        y_missile-=y_missile_speed

    if y_missile <= 0:
        y_missile = y_screen-130
        x_missile = 0
        is_fire = False

    # Affichage du joueur et de l'invader
    ecran.blit(player, (x_player,y_player))

    # affichage ecran
    show_score(scoreX, scoreY)
    pygame.display.update()

# vide le cache
pygame.quit()