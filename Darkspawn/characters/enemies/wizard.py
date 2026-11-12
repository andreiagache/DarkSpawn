
import pygame


class Wizard:

    def __init__(self, position):

        # Position is controlled by the level
        self.position = pygame.Vector2(position)

        # --------------------------------------------------
        # HEALTH
        # --------------------------------------------------

        self.max_hp = 50
        self.hp = self.max_hp


        # --------------------------------------------------
        # IDLE ANIMATION
        # --------------------------------------------------

        self.idle_frames = []

        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 125

        self.wizard_height = 500

        self.load_idle_animation()

    # --------------------------------------------------
    # LOAD IDLE ANIMATION
    # --------------------------------------------------

    def load_idle_animation(self):

        wizard_path = "assets/images/Enemies/"

        for i in range(1, 7):

            image = pygame.image.load(
                wizard_path + f"Wizard{i}.png"
            ).convert_alpha()

            # Preserve aspect ratio
            original_width, original_height = image.get_size()

            wizard_width = int(
                original_width
                * self.wizard_height
                / original_height
            )

            image = pygame.transform.scale(
                image,
                (
                    wizard_width,
                    self.wizard_height
                )
            )

            self.idle_frames.append(image)

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(self, dt):

        self.animation_timer += dt

        while self.animation_timer >= self.frame_duration:

            self.animation_timer -= self.frame_duration

            self.current_frame += 1

            if self.current_frame >= len(self.idle_frames):

                self.current_frame = 0

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self, screen):

        image = self.idle_frames[self.current_frame]

        rect = image.get_rect(
            midbottom=self.position
        )

        screen.blit(
            image,
            rect
        )

    # --------------------------------------------------
    # TAKE DAMAGE
    # --------------------------------------------------
    
    def take_damage(self, amount):

        self.hp -= amount

        # Prevent HP from going below zero
        self.hp = max(0, self.hp)


    def is_alive(self):

        return self.hp > 0
