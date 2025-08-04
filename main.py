import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont('Comic Sans MS', 30)
    score = 0
    current_lives = STARTING_LIVES
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.check_collision(player):
                if player.invulnerable == False:
                    current_lives -= 1
                    player.respawn()
                if current_lives == 0:
                    print("Game Over!")
                    sys.exit()
            for shot in shots:
                if asteroid.check_collision(shot):
                    asteroid.split()
                    shot.kill()
                    if asteroid.radius == ASTEROID_MIN_RADIUS:
                        score += SMALL_ASTEROIDS_POINTS
                    elif asteroid.radius == ASTEROID_MAX_RADIUS:
                        score += LARGE_ASTEROID_POINTS        
                    else:
                        score += MEDIUM_ASTEROID_POINTS


        screen.fill((0,0,0))

        for sprite in drawable:
            sprite.draw(screen)

        score_display = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_display, (20, 20))
        lives_display = font.render(f"Lives: {current_lives}", True, (255, 255, 255))
        screen.blit(lives_display, (20, 40))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
