
import pygame

from screens.main_menu import MainMenu
from screens.map import MapScreen
from screens.level1 import Level1

pygame.init()

# --------------------------------------------------
# WINDOW
# --------------------------------------------------

display_info = pygame.display.Info()

WIDTH = display_info.current_w
HEIGHT = display_info.current_h

screen = pygame.display.set_mode(
    (0, 0),
    pygame.FULLSCREEN
)

pygame.display.set_caption("Darkspawn")

clock = pygame.time.Clock()

# --------------------------------------------------
# SCREENS
# --------------------------------------------------

main_menu = MainMenu(screen)
map_screen = MapScreen(screen)
level1 = Level1(screen)

current_screen = "menu"

# --------------------------------------------------
# TRANSITION
# --------------------------------------------------

transition_alpha = 0
transition_speed = 8

transition_direction = 0
pending_screen = None

transition_surface = pygame.Surface(
    (WIDTH, HEIGHT)
)

transition_surface.fill((0, 0, 0))


def start_transition(target):

    global pending_screen
    global transition_direction

    # Start fading to black
    pending_screen = target
    transition_direction = 1


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

running = True

while running:

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # Ignore screen actions while transitioning
        if transition_direction != 0:

            continue

        # ----------------------------------------------
        # MAIN MENU
        # ----------------------------------------------

        if current_screen == "menu":

            action = main_menu.handle_event(event)

            if action == "new_game":

                start_transition("map")

            elif action == "continue":

                start_transition("map")

            elif action == "quit":

                running = False

        # ----------------------------------------------
        # MAP
        # ----------------------------------------------

        elif current_screen == "map":

            action = map_screen.handle_event(event)

            if action == "menu":

                start_transition("menu")

            elif action == "encounter":

                start_transition("level1")

        # ----------------------------------------------
        # LEVEL 1
        # ----------------------------------------------

        elif current_screen == "level1":

            action = level1.handle_event(event)

            if action == "map":

                start_transition("map")

    # --------------------------------------------------
    # TIME
    # --------------------------------------------------

    dt = clock.tick(60)

    # --------------------------------------------------
    # LEVEL UPDATE
    # --------------------------------------------------

    if current_screen == "level1":

        level1.update(dt)

    # --------------------------------------------------
    # TRANSITION UPDATE
    # --------------------------------------------------

    if transition_direction == 1:

        # Fade to black
        transition_alpha += transition_speed

        if transition_alpha >= 255:

            transition_alpha = 255

            # Switch screen while completely black
            current_screen = pending_screen

            pending_screen = None

            # Begin fading from black
            transition_direction = -1

    elif transition_direction == -1:

        # Fade from black
        transition_alpha -= transition_speed

        if transition_alpha <= 0:

            transition_alpha = 0

            transition_direction = 0

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    if current_screen == "menu":

        main_menu.draw()

    elif current_screen == "map":

        map_screen.draw()

    elif current_screen == "level1":

        level1.draw()

    # --------------------------------------------------
    # TRANSITION DRAW
    # --------------------------------------------------

    if transition_alpha > 0:

        transition_surface.set_alpha(
            transition_alpha
        )

        screen.blit(
            transition_surface,
            (0, 0)
        )

    # --------------------------------------------------
    # UPDATE DISPLAY
    # --------------------------------------------------

    pygame.display.flip()

# --------------------------------------------------
# EXIT
# --------------------------------------------------

pygame.quit()
