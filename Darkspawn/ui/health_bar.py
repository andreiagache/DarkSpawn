
import pygame


class HealthBar:

    def __init__(self, x, y, width, height):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.background_color = (45, 35, 35)
        self.health_color = (160, 35, 45)
        self.border_color = (210, 190, 170)

        self.font = pygame.font.Font(None, 24)

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self, screen, current_hp, max_hp):

        # Background
        pygame.draw.rect(
            screen,
            self.background_color,
            self.rect
        )

        # Calculate health percentage
        health_percentage = current_hp / max_hp

        # Calculate fill width
        fill_width = int(
            self.rect.width * health_percentage
        )

        # Health fill
        health_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            fill_width,
            self.rect.height
        )

        pygame.draw.rect(
            screen,
            self.health_color,
            health_rect
        )

        # Border
        pygame.draw.rect(
            screen,
            self.border_color,
            self.rect,
            2
        )

        # HP text
        hp_text = self.font.render(
            f"{current_hp}/{max_hp}",
            True,
            (255, 255, 255)
        )

        text_rect = hp_text.get_rect(
            center=self.rect.center
        )

        screen.blit(
            hp_text,
            text_rect
        )
