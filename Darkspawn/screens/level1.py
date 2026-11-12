
import pygame

from ui.health_bar import HealthBar
from characters.player import Player
from characters.enemies.wizard import Wizard


class Level1:

    def __init__(self, screen):

        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()

        # --------------------------------------------------
        # BACKGROUND
        # --------------------------------------------------

        self.background = pygame.image.load(
            "assets/images/Level1/level1.png"
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            (self.WIDTH, self.HEIGHT)
        )

        # --------------------------------------------------
        # COMBAT RESULT TEXT IMAGES
        # --------------------------------------------------

        result_path = "assets/images/Level1/"

        self.victory_image = pygame.image.load(
            result_path + "Victory.png"
        ).convert_alpha()

        self.defeat_image = pygame.image.load(
            result_path + "Defeat.png"
        ).convert_alpha()

        # --------------------------------------------------
        # CHARACTERS
        # --------------------------------------------------

        self.player = Player(
            (
                self.WIDTH // 5,
                self.HEIGHT - 300
            )
        )

        self.enemy = Wizard(
            (
                self.WIDTH * 4 // 5.5,
                self.HEIGHT - 300
            )
        )

        # --------------------------------------------------
        # HEALTH BARS
        # --------------------------------------------------

        # Player health bar
        self.player_health_bar = HealthBar(
            60,
            50,
            300,
            30
        )

        # Wizard health bar
        self.enemy_health_bar = HealthBar(
            int(self.enemy.position.x - 130),
            int(self.enemy.position.y - self.enemy.wizard_height - 40),
            260,
            30
        )

        # --------------------------------------------------
        # PAUSE MENU
        # --------------------------------------------------

        self.paused = False

        # Dark overlay
        self.pause_overlay = pygame.Surface(
            (self.WIDTH, self.HEIGHT),
            pygame.SRCALPHA
        )

        self.pause_overlay.fill(
            (0, 0, 0, 180)
        )

        # --------------------------------------------------
        # PAUSE BUTTONS
        # --------------------------------------------------

        self.BUTTON_PATH = "assets/images/darkspawn_buttons/"

        self.pause_button_width = 350
        self.pause_button_height = 90

        # Resume normal
        self.resume_normal = pygame.transform.scale(
            pygame.image.load(
                self.BUTTON_PATH + "resume_normal.png"
            ).convert_alpha(),
            (
                self.pause_button_width,
                self.pause_button_height
            )
        )

        # Resume selected
        self.resume_selected = pygame.transform.scale(
            pygame.image.load(
                self.BUTTON_PATH + "resume_selected.png"
            ).convert_alpha(),
            (
                self.pause_button_width,
                self.pause_button_height
            )
        )

        # Exit normal
        self.exit_normal = pygame.transform.scale(
            pygame.image.load(
                self.BUTTON_PATH + "exit_normal.png"
            ).convert_alpha(),
            (
                self.pause_button_width,
                self.pause_button_height
            )
        )

        # Exit selected
        self.exit_selected = pygame.transform.scale(
            pygame.image.load(
                self.BUTTON_PATH + "exit_selected.png"
            ).convert_alpha(),
            (
                self.pause_button_width,
                self.pause_button_height
            )
        )

        # --------------------------------------------------
        # BUTTON POSITIONS
        # --------------------------------------------------

        center_x = self.WIDTH // 2
        center_y = self.HEIGHT // 2

        self.resume_rect = pygame.Rect(
            center_x - self.pause_button_width // 2,
            center_y - self.pause_button_height - 15,
            self.pause_button_width,
            self.pause_button_height
        )

        self.exit_rect = pygame.Rect(
            center_x - self.pause_button_width // 2,
            center_y + 15,
            self.pause_button_width,
            self.pause_button_height
        )

        # --------------------------------------------------
        # COMBAT STATE
        # --------------------------------------------------

        self.combat_state = "ongoing"


    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    def handle_event(self, event):

        # --------------------------------------------------
        # ESCAPE: PAUSE / RESUME
        # --------------------------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.paused = not self.paused

                return None

        # --------------------------------------------------
        # PAUSE MENU EVENTS
        # --------------------------------------------------

        if self.paused:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    # Resume
                    if self.resume_rect.collidepoint(event.pos):

                        self.paused = False

                    # Exit to map
                    elif self.exit_rect.collidepoint(event.pos):

                        self.paused = False

                        return "map"

            # Ignore gameplay events while paused
            return None

        # --------------------------------------------------
        # NORMAL GAMEPLAY EVENTS
        # --------------------------------------------------

        if event.type == pygame.KEYDOWN:

            # BASIC ATTACK
            if event.key == pygame.K_SPACE:

                if self.combat_state == "ongoing":

                    self.player.start_attack(
                        self.enemy.position
                    )

            # TEMPORARY: Damage Wizard
            elif event.key == pygame.K_h:

                self.enemy.take_damage(10)

            # TEMPORARY: Damage Player
            elif event.key == pygame.K_j:

                self.player.take_damage(10)

        return None
    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(self, dt):

        # Freeze everything while paused
        if self.paused:
            return

        # Don't update characters after combat ends
        if self.combat_state != "ongoing":
            return

        # --------------------------------------------------
        # CHECK DEATH
        # --------------------------------------------------

        if not self.player.is_alive():

            self.combat_state = "defeat"
            return

        if not self.enemy.is_alive():

            self.combat_state = "victory"
            return

        # --------------------------------------------------
        # CHARACTERS
        # --------------------------------------------------

        self.player.update(dt)
        self.enemy.update(dt)

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self):

        # --------------------------------------------------
        # BACKGROUND
        # --------------------------------------------------

        self.screen.blit(
            self.background,
            (0, 0)
        )

            # --------------------------------------------------
        # CHARACTERS
        # --------------------------------------------------

        if self.player.is_alive():

            self.player.draw(self.screen)

        if self.enemy.is_alive():

            self.enemy.draw(self.screen)

        # --------------------------------------------------
        # HEALTH BARS
        # --------------------------------------------------

        self.player_health_bar.draw(
            self.screen,
            self.player.hp,
            self.player.max_hp
        )

        self.enemy_health_bar.draw(
            self.screen,
            self.enemy.hp,
            self.enemy.max_hp
        )

                # --------------------------------------------------
        # COMBAT RESULT
        # --------------------------------------------------

        if self.combat_state == "victory":

            image = self.victory_image

        elif self.combat_state == "defeat":

            image = self.defeat_image

        else:

            image = None

        if image:

            image_rect = image.get_rect(
                center=(
                    self.WIDTH // 2,
                    self.HEIGHT // 2
                )
            )

            self.screen.blit(
                image,
                image_rect
            )

        # --------------------------------------------------
        # PAUSE MENU
        # --------------------------------------------------

        if self.paused:

            # Darken the level
            self.screen.blit(
                self.pause_overlay,
                (0, 0)
            )

            mouse_position = pygame.mouse.get_pos()

            # Resume hover
            if self.resume_rect.collidepoint(mouse_position):

                resume_button = self.resume_selected

            else:

                resume_button = self.resume_normal

            # Exit hover
            if self.exit_rect.collidepoint(mouse_position):

                exit_button = self.exit_selected

            else:

                exit_button = self.exit_normal

            # Draw Resume
            self.screen.blit(
                resume_button,
                self.resume_rect
            )

            # Draw Exit
            self.screen.blit(
                exit_button,
                self.exit_rect
            )
