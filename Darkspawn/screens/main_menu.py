
import pygame


class MainMenu:

    def __init__(self, screen):

        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()

        self.BUTTON_PATH = "assets/images/darkspawn_buttons/"

        self.menu_actions = ["new_game", "continue", "quit"]

        self.menu_button_width = 450
        self.menu_button_height = 100
        self.menu_button_spacing = 110

        # Background
        self.menu_background = pygame.image.load(
            "assets/images/startscreen.png"
        ).convert()

        self.menu_background = pygame.transform.scale(
            self.menu_background, (self.WIDTH, self.HEIGHT)
        )

        # Buttons
        size = (self.menu_button_width, self.menu_button_height)

        self.menu_normal_buttons = []
        self.menu_selected_buttons = []

        for name in ("new_game", "continue", "quit"):

            normal = pygame.image.load(
                self.BUTTON_PATH + name + "_normal.png"
            ).convert_alpha()

            selected = pygame.image.load(
                self.BUTTON_PATH + name + "_selected.png"
            ).convert_alpha()

            self.menu_normal_buttons.append(
                pygame.transform.scale(normal, size)
            )

            self.menu_selected_buttons.append(
                pygame.transform.scale(selected, size)
            )

        # Button positions
        self.menu_button_rects = []

        for i in range(len(self.menu_actions)):

            x = self.WIDTH // 2 - self.menu_button_width // 2
            y = int(self.HEIGHT * 0.65) + i * self.menu_button_spacing

            self.menu_button_rects.append(
                pygame.Rect(
                    x, y,
                    self.menu_button_width,
                    self.menu_button_height
                )
            )

        # Keyboard selection
        self.selected_button = 0

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            # Move selection up
            if event.key == pygame.K_UP:
                self.selected_button = (
                    self.selected_button - 1
                ) % len(self.menu_actions)

            # Move selection down
            elif event.key == pygame.K_DOWN:
                self.selected_button = (
                    self.selected_button + 1
                ) % len(self.menu_actions)

            # Activate selected button
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.menu_actions[self.selected_button]

        return None

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self):

        self.screen.blit(self.menu_background, (0, 0))

        for i, rect in enumerate(self.menu_button_rects):

            if i == self.selected_button:
                button = self.menu_selected_buttons[i]
            else:
                button = self.menu_normal_buttons[i]

            self.screen.blit(button, rect)
