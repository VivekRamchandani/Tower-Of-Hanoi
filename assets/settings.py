import pygame
import sys

from .gui.dialog_box import DialogBox
from .gui.blocks import ColorBlock, Button, TransparentBlock


class Setting:
    """Class to Create and Manage Setting Screen"""
    def __init__(self, screen_width, screen_height, position):
        """To Create and manage setting screen"""
        self.display = False

        # Screen
        self.surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = position

        # Dialog Box
        self.dialog_box = DialogBox(300, 170, self.surface_rect.center)

        # Quit Button
        button_position = self.surface_rect.center[0], self.surface_rect.center[1] + 130
        self.quit_button = Button(300, 50, button_position, "Exit")

        # Restart Button
        button_position = self.surface_rect.center[0], self.surface_rect.center[1] - 130
        self.restart_button = Button(300, 50, button_position, "Restart")

        # Settings
        self._selected_bg_color_block = self.dialog_box.bg_color_blocks[0]
        self.main_bg_color = (255, 255, 255)

        self._selected_color_block = self.dialog_box.block_color_blocks[0]
        self.tower_block_color = self._selected_color_block.color

        # Highlighting Blocks
        self._tblock_for_bg = TransparentBlock(self._selected_bg_color_block.width,
                                               self._selected_bg_color_block.rect.center)
        self.tower_color = (60, 60, 60)
        self.restart_flag = False

    def check_events(self, event):
        """Check Settings Events"""
        # Keyboard Events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.display = False
        # Mouse Events
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check Mouse Collisions
            mouse_pos = pygame.mouse.get_pos()
            # With Dialog Box
            if self.dialog_box.rect.collidepoint(mouse_pos):
                self._check_dialog_box_collisions(mouse_pos)
            # With Quit Button
            elif self.quit_button.rect.collidepoint(mouse_pos):
                sys.exit()
            # With Restart Button
            elif self.restart_button.rect.collidepoint(mouse_pos):
                self.restart_flag = True

    def _check_dialog_box_collisions(self, mouse_pos):
        clicked_block, block_type = self._get_clicked_block(mouse_pos)
        if block_type == "Block Color":
            self._selected_color_block = clicked_block
            self.tower_block_color = clicked_block.color
        elif block_type == "Background Color":
            self._selected_bg_color_block = clicked_block
            self._tblock_for_bg.update(self._selected_bg_color_block.rect.center)
            self.main_bg_color = self._selected_bg_color_block.color

    def _get_clicked_block(self, mouse_pos):
        """Return the block that is clicked"""
        clicked_block: ColorBlock | None = None
        block_type: str | None = None
        for block in self.dialog_box.block_color_blocks:
            clicked = block.rect.collidepoint(mouse_pos)
            if clicked:
                clicked_block = block
                block_type = "Block Color"
                return clicked_block, block_type

        for block in self.dialog_box.bg_color_blocks:
            clicked = block.rect.collidepoint(mouse_pos)
            if clicked:
                clicked_block = block
                block_type = "Background Color"

        return clicked_block, block_type

    def update(self):
        if self.main_bg_color == (255, 255, 255):
            self.tower_color = (60, 60, 60)
        else:
            self.tower_color = (220, 220, 220)

    def blit_me(self, surface: pygame.Surface):
        # Create Settings Background
        self.surface.fill((50, 50, 50, 230))
        surface.blit(self.surface, self.surface_rect)

        # Create Dialog Box
        self.dialog_box.draw_me(surface)

        # Create Quit Button
        self.quit_button.draw_me(surface, (255, 255, 255))

        # Create Restart Button
        self.restart_button.draw_me(surface, (255, 255, 255))

        # Highlight Selected Blocks
        self._tblock_for_bg.draw_me(surface, (215, 215, 215))
        self._selected_color_block.selected = True
        self._selected_color_block.draw_me(surface)
