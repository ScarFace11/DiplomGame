# trap.py
import pygame
from support import import_sprite

class TrapBase(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.size = size
        self.frame_index = 0
        self.image = None
        self.mask = None
        self.rect = pygame.Rect(pos, (size, size))

    def _animate(self, sprites, animation_delay):
        sprite_index = (self.frame_index // animation_delay) % len(sprites)
        self.image = sprites[sprite_index]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.frame_index += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.frame_index // animation_delay >= len(sprites):
            self.frame_index = 0

    def update(self):
        pass  # Этот метод будет переопределен в дочерних классах

class Laser(TrapBase):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.blade_img = import_sprite("Sprite/trap/laser")
        self.animation_delay = 3
        self.status = 'activated'
        self.image = self.blade_img[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)

    def _animate(self):
        super()._animate(self.blade_img, self.animation_delay)

    def update(self):
        self._animate()

class Spike(TrapBase):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self._import_spike_assets()
        self.last_sprite_change_time = pygame.time.get_ticks()
        self.status = 'neutral'
        self.animation_delays = {'neutral': 1, 'retractable': 20, 'activated': 1, 'to_hide': 120}
        self.animation_start_time = 0

    def _import_spike_assets(self):
        character_path = 'Sprite/trap/spike'
        self.animations = {'neutral': [], 'retractable': [], 'activated': [], 'to_hide': []}
        for animation in self.animations.keys():
            full_path = character_path + '/' + animation
            self.animations[animation] = import_sprite(full_path)

    def _update_status(self):
        current_time = pygame.time.get_ticks()
        if self.status == 'neutral' and current_time - self.last_sprite_change_time >= 5000:
            self.last_sprite_change_time = current_time
            self.status = 'retractable'
            self.animation_start_time = current_time
        elif self.status == 'retractable' and current_time - self.last_sprite_change_time >= 1000:
            self.last_sprite_change_time = current_time
            self.status = 'activated'
            self.animation_start_time = current_time
        elif self.status == 'activated' and current_time - self.last_sprite_change_time >= 5000:
            self.last_sprite_change_time = current_time
            self.status = 'to_hide'
            self.animation_start_time = current_time
        elif self.status == 'to_hide' and current_time - self.animation_start_time >= self.animation_delays['to_hide']:
            self.last_sprite_change_time = current_time
            self.status = 'neutral'
            self.animation_start_time = current_time

    def _animate(self):
        super()._animate(self.animations[self.status], self.animation_delays[self.status])

    def update(self):
        self._update_status()
        self._animate()
