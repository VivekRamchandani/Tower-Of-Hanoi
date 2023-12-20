import pygame

from .blocks import TowerBlock


class Tower:
    """Class to create and manage towers"""
    def __init__(self, position, number):
        self.number = number    # <-- Just for debugging

        # Setting up tower space
        self.space_rect = pygame.Rect(0, 0, 150, 200)
        self.space_rect.center = position

        # Setting up tower
        self.width, self.height = 10, 160
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # Positioning tower in tower space
        self.rect.midbottom = self.space_rect.midbottom

        self.block_stack = []

    def draw_me(self, surface: pygame.Surface, color: tuple[int, int, int]):
        """Draws itself"""
        pygame.draw.rect(surface, color, self.rect, border_radius=2)

    def add(self, block: TowerBlock):
        """Adds block to the tower"""
        if len(self.block_stack) == 0 or self.block_stack[0].weight > block.weight:
            # Positioning the block at the top of stack
            block.rect.midbottom = self.rect.midbottom
            block.rect.y -= (len(self.block_stack) * 20)

            # Change the last valid position to current position
            block.last_valid_position = block.rect.center

            # If Belonging to different stack or no stack
            if block.belongs_to_stack != self.block_stack:
                if block.belongs_to_stack:
                    block.belongs_to_stack.pop(0)       # Remove from other stack
                self.block_stack.insert(0, block)   # Add to stack of this tower

            block.belongs_to_stack = self.block_stack

            return True
        else:
            # If block can't be placed in this stack then place it back
            block.rect.center = block.last_valid_position
