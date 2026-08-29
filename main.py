import pygame
from pygame.locals import *
import asyncio
import random

pygame.init()


async def main():
    S_WIDTH, S_HEIGHT = 800, 600
    screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    pygame.display.set_caption("Mosquito Shooter")
    clock = pygame.time.Clock()

    class Alien:
        def __init__(self, x, y):
            self.image = pygame.image.load("mosquito1.webp").convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 20))

            self.dead_image = pygame.image.load("mosquito2.webp").convert_alpha()
            self.dead_image = pygame.transform.scale(self.dead_image, (30, 20))

            self.rect = self.image.get_rect(topleft=(x, y))
            self.dead = False
            self.dead_time = 0

        def move(self, speed):
            if not self.dead:
                self.rect.x += speed

        def kill(self):
            self.dead = True
            self.dead_time = pygame.time.get_ticks()

        def update(self):
            if self.dead:
                if pygame.time.get_ticks() - self.dead_time >= 1500:
                    return True

            return False

        def draw(self):
            if self.dead:
                screen.blit(self.dead_image, self.rect)
            else:
                screen.blit(self.image, self.rect)


    class Bullet:
        def __init__(self, x, y):
            self.image = pygame.image.load("sunbeam.webp").convert_alpha()
            self.image = pygame.transform.scale(self.image, (15, 37))
            self.rect = self.image.get_rect(center=(x, y))

        def move(self):
            self.rect.y -= 8
        
        def draw(self):
            screen.blit(self.image, self.rect)

    class RainbowBullet:
        def __init__(self, x, y):
            self.image = pygame.image.load("rainbow.webp").convert_alpha()
            self.image = pygame.transform.scale(self.image, (15, 35))
            self.rect = self.image.get_rect(center=(x, y))

        def move(self):
            self.rect.y -= 8

        def draw(self):
            screen.blit(self.image, self.rect)

    class Lollipop:
            def __init__(self, x, y):
                self.image = pygame.image.load("lollipop.webp").convert_alpha()
                self.image = pygame.transform.scale(self.image, (25, 40))
                self.rect = self.image.get_rect(center=(x, y))
    
            def move(self):
                self.rect.y -= 8
    
            def draw(self):
                screen.blit(self.image, self.rect)
    

    def create_aliens():
        aliens = []

        for row in range(4):
            for col in range(8):
                aliens.append(
                    Alien(160 + col * 70, 60 + row * 45)
                )

        return aliens

    player = pygame.Rect(380, 510, 40, 20)
    aliens = create_aliens()
    bullets = []
    rainbow_bullets = []
    lollipops = []

    player_image = pygame.image.load("solietta.webp").convert_alpha()
    player_image = pygame.transform.scale(player_image, (100, 125))

    player = player_image.get_rect(center=(S_WIDTH // 2, S_HEIGHT - 40))

    #MAIN


    status = "title"
    alien_speed = 2
    alien_direction = 1
    pts = 0
    totalscore = 0
    level = 1
    tut = ["Welcome to the mosquito shooter of your dreams! (Press SPACE to continue)", 
                "Use arrow keys to move.", 
                "Press SPACE to shoot.", 
                "There is a point system here.",
                "When you reach level 3, you will be able to shoot new types of bullets!",
                "Press R to shoot those.",
                "Press Q when you get to level 6 to get a third type of bullets.",
                "Press ENTER to start the game!"
                ]
    tut_index = 0

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
                    status = "tut"

                elif event.key == K_SPACE and status == "tut":
                    if tut_index < len(tut) - 1:
                        tut_index += 1

                elif event.key == K_RETURN and status == "tut" and tut_index == len(tut) - 1:
                    status = "game"

                elif event.key == K_SPACE and status == "game":
                    bullets.append(Bullet(player.centerx - 2, player.top))

                elif event.key == K_r and status == "game" and level >= 3:
                    rainbow_bullets.append(RainbowBullet(player.centerx - 2,player.top))

                elif event.key == K_q and status == "game" and level >= 6:
                    lollipops.append(Lollipop(player.centerx - 2,player.top))

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

        elif status == "tut":

            screen.fill((0, 0, 0))

            text = font.render(
            tut[tut_index],
                True,
                (255, 255, 255)
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(S_WIDTH // 2, S_HEIGHT // 2)
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
                        alien.kill()

                        pts += 1

                        if pts >= level *10:
                            totalscore += pts
                            pts = 0

                            level += 1
                            alien_speed += 0.5

                        break

            for bullet in rainbow_bullets:
                bullet.move()

            for bullet in rainbow_bullets[:]:
            
                for alien in aliens[:]:
            
                    if bullet.rect.colliderect(alien.rect):
            
                        rainbow_bullets.remove(bullet)
                        alien.kill()
            
                        pts += 1

                        if aliens and random.random() < 0.3:
                            random_alien = random.choice(aliens)
                            if random_alien != alien and not random_alien.dead:
                                random_alien.kill()
                                pts += 1
            
                        if pts >= level *10:
                            totalscore += pts
                            pts = 0
            
                            level += 1
                            alien_speed += 0.5
            
                        break

            for bullet in lollipops:
                bullet.move()

                if bullet.rect.bottom < 0:
                    lollipops.remove(bullet)

            for bullet in lollipops[:]:
                for alien in aliens[:]:

                    if bullet.rect.colliderect(alien.rect):

                        lollipops.remove(bullet)
                        alien.kill()
                        pts += 1

                        closest_alien = None
                        closest_distance = 80

                        for other_alien in aliens:
                            if other_alien != alien and not other_alien.dead:

                                distance_x = other_alien.rect.centerx - alien.rect.centerx
                                distance_y = other_alien.rect.centery - alien.rect.centery

                                distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

                                if distance < closest_distance:
                                    closest_distance = distance
                                    closest_alien = other_alien

                        if closest_alien is not None:
                            closest_alien.kill()
                            pts += 1

                        break

            for alien in aliens[:]:
                if alien.update():
                    aliens.remove(alien)

            if len(aliens) == 0:

                aliens = create_aliens()
                alien_speed += 0.5
                alien_direction = 1

            screen.fill((0, 0, 0))

            for alien in aliens:
                alien.draw()

            for bullet in bullets:
                bullet.draw()

            for bullet in rainbow_bullets:
                bullet.draw()

            for bullet in lollipops:
                bullet.draw()

            screen.blit(player_image, player)

            score_text = font.render(
                f"Score: {totalscore}",
                True,
                (255, 255, 255)
            )

            points_text = font.render(
                f"Points: {pts}",
                True,
                (255, 255, 255)
            )

            level_text = font.render(
                f"Level: {level}",
                True,
                (255, 255, 255)
            )

            screen.blit(score_text, (10, 10))
            screen.blit(points_text, (10, 40))
            screen.blit(level_text, (10, 70))

        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())