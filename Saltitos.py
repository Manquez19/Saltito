import pygame
import random

# Configuración de la ventana
WIDTH = 400
HEIGHT = 600
FPS = 30

# Configuración de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Carga de recursos
font_name = pygame.font.match_font('arial')

# Función para mostrar el puntaje en la pantalla
def draw_score(score):
    font = pygame.font.Font(font_name, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, 50)
    screen.blit(text, text_rect)

# Clase del jugador (ave)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/dolarcito.png").convert_alpha()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = 0
    
    def update(self):
        self.velocity += GRAVITY  # Ajusta el valor de GRAVITY para controlar la gravedad
        self.rect.y += self.velocity

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -10

# Clase de los tubos
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 400))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - 200)
        else:
            self.rect.topleft = (x, y + 200)
    
    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# Creación de grupos de sprites
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# Creación del jugador
player = Player()
all_sprites.add(player)

# Variables de juego
score = 0

# Gravedad
GRAVITY = 0.5 # Ajusta el valor para controlar la gravedad

# Bucle principal del juego
running = True
while running:
    # Mantener la frecuencia de fotogramas
    clock.tick(FPS)
    
    # Eventos del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
    
    # Actualización de sprites
    all_sprites.update()
    
    # Generación de nuevos tubos
    if len(pipes) < 5:
        if random.randint(0, 100) < 20:
            pipe = Pipe(WIDTH, random.randint(100, 400))
            pipes.add(pipe)
            all_sprites.add(pipe)
    
    # Colisiones entre el jugador y los tubos
    if pygame.sprite.spritecollide(player, pipes, False):
        running = False
    
    # Comprobación de puntuación
    for pipe in pipes:
        if pipe.rect.right < player.rect.left and not pipe.rect.y < player.rect.y < pipe.rect.bottom:
            score += 1
    
    # Renderizado de la pantalla
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_score(score)
    pygame.display.flip()

pygame.quit()
