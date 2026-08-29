import pygame
from pygame.locals import *
import asyncio

pygame.init()


async def main():
    S_WIDTH, S_HEIGHT = 800, 600
    screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    pygame.display.set_caption("Mosquito Shooter")
    clock = pygame.time.Clock()

    class Alien:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 30, 20)

        def move(self, speed):
            self.rect.x += speed

        def draw(self):
            pygame.draw.rect(screen, (255, 50, 50), self.rect)

    class Bullet:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 5, 10)

        def move(self):
            self.rect.y -= 8

        def draw(self):
            pygame.draw.rect(screen, (255, 255, 255), self.rect)

    player = pygame.Rect(380, 550, 40, 20)

    aliens = []

    for row in range(4):
        for col in range(8):
            aliens.append(
                Alien(160 + col * 70, 60 + row * 45)
            )

    status = "title"
    bullets = []
    alien_speed = 2
    alien_direction = 1
    score = 0

    font = pygame.font.Font(None, 30)
    title_font = pygame.font.Font(None, 60)

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    running = False

                elif event.key == K_RETURN and status == "title":
                    status = "game"

                elif event.key == K_SPACE and status == "game":
                    bullets.append(
                        Bullet(player.centerx - 2, player.top)
                    )

        if status == "title":

            screen.fill((0, 0, 0))

            title = title_font.render(
                "Mosquito Shooter",
                True,
                (255, 255, 255)
            )

            instructions = font.render(
                "Press ENTER to start",
                True,
                (255, 255, 255)
            )

            screen.blit(
                title,
                title.get_rect(
                    center=(S_WIDTH // 2, 250)
                )
            )

            screen.blit(
                instructions,
                instructions.get_rect(
                    center=(S_WIDTH // 2, 330)
                )
            )

        elif status == "game":
            keys = pygame.key.get_pressed()
            if keys[K_LEFT] or keys[K_a]:
                player.x -= 5
            if keys[K_RIGHT] or keys[K_d]:
                player.x += 5
                
            player.clamp_ip(screen.get_rect())

            hit_edge = False

            for alien in aliens:

                if alien.rect.right >= S_WIDTH - 20 and alien_direction > 0:
                    hit_edge = True

                if alien.rect.left <= 20 and alien_direction < 0:
                    hit_edge = True

            if hit_edge:
                alien_direction *= -1

            for alien in aliens:
                alien.move(alien_speed * alien_direction)

            for bullet in bullets[:]:

                bullet.move()

                if bullet.rect.bottom < 0:
                    bullets.remove(bullet)

            for bullet in bullets[:]:

                for alien in aliens[:]:

                    if bullet.rect.colliderect(alien.rect):

                        bullets.remove(bullet)
                        aliens.remove(alien)
                        score += 1
                        break

            screen.fill((0, 0, 0))

            for alien in aliens:
                alien.draw()

            for bullet in bullets:
                bullet.draw()

            pygame.draw.rect(
                screen,
                (50, 255, 100),
                player
            )

            score_text = font.render(
                f"Score: {score}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                score_text,
                (10, 10)
            )

        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())