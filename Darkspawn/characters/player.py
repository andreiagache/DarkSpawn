
import pygame


class Player:

    def __init__(self, position):

        # Position is controlled by the level
        self.position = pygame.Vector2(position)

        # --------------------------------------------------
        # HEALTH
        # --------------------------------------------------

        self.max_hp = 100
        self.hp = self.max_hp

        # --------------------------------------------------
        # IDLE ANIMATION
        # --------------------------------------------------

        self.idle_frames = []

        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 125

        self.character_height = 500

        self.load_idle_animation()

        # --------------------------------------------------
        # ATTACK IMAGE
        # --------------------------------------------------

        self.attack_image = pygame.image.load(
            "assets/images/Main_character/Dagger_slash.png"
        ).convert_alpha()

        original_width, original_height = self.attack_image.get_size()

        attack_width = int(
            original_width * self.character_height / original_height
        )

        self.attack_image = pygame.transform.scale(
            self.attack_image,
            (attack_width, self.character_height)
        )

        # --------------------------------------------------
        # ATTACK SETTINGS
        # --------------------------------------------------

        self.is_attacking = False
        self.attack_phase = None
        self.attack_timer = 0

        self.original_position = self.position.copy()
        self.attack_position = self.position.copy()

        self.snap_distance = 600

        self.vanish_duration = 250
        self.slash_duration = 400
        self.recovery_duration = 250

    # --------------------------------------------------
    # LOAD IDLE ANIMATION
    # --------------------------------------------------

    def load_idle_animation(self):

        character_path = "assets/images/Main_character/"

        for i in range(1, 7):

            image = pygame.image.load(
                character_path + f"Idle{i}.png"
            ).convert_alpha()

            original_width, original_height = image.get_size()

            character_width = int(
                original_width
                * self.character_height
                / original_height
            )

            image = pygame.transform.scale(
                image,
                (character_width, self.character_height)
            )

            self.idle_frames.append(image)

    # --------------------------------------------------
    # START ATTACK
    # --------------------------------------------------

    def start_attack(self, target_position):

        if self.is_attacking or not self.is_alive():
            return

        self.is_attacking = True
        self.attack_phase = "vanishing"
        self.attack_timer = 0

        self.original_position = self.position.copy()

        # Determine horizontal direction
        direction = (
            1 if target_position.x > self.position.x else -1
        )

        # Calculate teleport destination
        self.attack_position = pygame.Vector2(
            self.position.x + direction * self.snap_distance,
            self.position.y
        )

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(self, dt):

        # --------------------------------------------------
        # ATTACK ANIMATION
        # --------------------------------------------------

        if self.is_attacking:

            self.attack_timer += dt

            # VANISH BEFORE TELEPORTING
            if self.attack_phase == "vanishing":

                if self.attack_timer >= self.vanish_duration:

                    self.position = self.attack_position.copy()

                    self.attack_phase = "slash"
                    self.attack_timer = 0

            # HOLD SLASH ANIMATION
            elif self.attack_phase == "slash":

                if self.attack_timer >= self.slash_duration:

                    self.position = self.original_position.copy()

                    self.attack_phase = "recovery"
                    self.attack_timer = 0

            # SHORT RECOVERY
            elif self.attack_phase == "recovery":

                if self.attack_timer >= self.recovery_duration:

                    self.is_attacking = False
                    self.attack_phase = None
                    self.attack_timer = 0

            return

        # --------------------------------------------------
        # IDLE ANIMATION
        # --------------------------------------------------

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

        # Player is invisible during the teleport delay
        if self.is_attacking and self.attack_phase == "vanishing":
            return

        if self.is_attacking and self.attack_phase == "slash":

            image = self.attack_image

        else:

            image = self.idle_frames[self.current_frame]

        rect = image.get_rect(
            midbottom=self.position
        )

        screen.blit(image, rect)

    # --------------------------------------------------
    # TAKE DAMAGE
    # --------------------------------------------------

    def take_damage(self, amount):

        self.hp -= amount
        self.hp = max(0, self.hp)

    def is_alive(self):

        return self.hp > 0
