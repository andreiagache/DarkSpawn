
import pygame


class MapScreen:

    def __init__(self, screen):

        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()

        # --------------------------------------------------
        # BACKGROUND
        # --------------------------------------------------

        self.map_background = pygame.image.load(
            "assets/images/map.png"
        ).convert()

        self.map_background = pygame.transform.scale(
            self.map_background,
            (self.WIDTH, self.HEIGHT)
        )

        # --------------------------------------------------
        # BACK BUTTON
        # --------------------------------------------------

        self.BUTTON_PATH = "assets/images/darkspawn_buttons/"

        self.back_button_width = 350
        self.back_button_height = 90

        self.back_normal = pygame.transform.scale(
            pygame.image.load(
                self.BUTTON_PATH + "back_normal.png"
            ).convert_alpha(),
            (
                self.back_button_width,
                self.back_button_height
            )
        )

        self.back_selected = pygame.transform.scale(
            pygame.image.load(
                self.BUTTON_PATH + "back_selected.png"
            ).convert_alpha(),
            (
                self.back_button_width,
                self.back_button_height
            )
        )

        self.back_button_rect = pygame.Rect(
            30,
            self.HEIGHT - self.back_button_height - 30,
            self.back_button_width,
            self.back_button_height
        )

        # --------------------------------------------------
        # MAP LOCATIONS
        # --------------------------------------------------

        self.map_locations = [
            pygame.Vector2(
                self.WIDTH * 0.505,
                self.HEIGHT * 0.845
            )
        ]

        self.selected_location = None

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                return "menu"

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                # Back button
                if self.back_button_rect.collidepoint(event.pos):
                    return "menu"

                # Map locations
                mouse_position = pygame.Vector2(event.pos)

                for i, location in enumerate(self.map_locations):

                    if mouse_position.distance_to(location) <= 30:

                        self.selected_location = i

                        return "encounter"

        return None

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self):

        # Background
        self.screen.blit(
            self.map_background,
            (0, 0)
        )

        # # Map locations
        # for i, location in enumerate(self.map_locations):

        #     color = (
        #         (255, 50, 50)
        #         if i == self.selected_location
        #         else (255, 220, 170)
        #     )

        #     pygame.draw.circle(
        #         self.screen,
        #         color,
        #         (int(location.x), int(location.y)),
        #         8
        #     )

        # Back button hover
        if self.back_button_rect.collidepoint(
            pygame.mouse.get_pos()
        ):

            button = self.back_selected

        else:

            button = self.back_normal

        self.screen.blit(
            button,
            self.back_button_rect
        )
