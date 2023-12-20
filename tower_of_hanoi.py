import pygame
import sys

from assets.settings import Setting
from assets.gui.towers import Tower
from assets.gui.blocks import TowerBlock


class TowerOfHanoi:
    """Class to manage assets and behaviour of game"""
    def __init__(self):
        """Initialize game and create game resources"""
        # Game Screen
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        pygame.display.set_caption("Tower of Hanoi")

        # Setting Screen
        self.setting = Setting(self.screen_width, self.screen_height, self.screen_rect.center)
        self.setting.display = False

        # Initialize Tower
        self.towers: list[Tower] = []
        self._create_towers()

        # Initialize blocks
        self.blocks = []
        self.moving_block: TowerBlock | None = None
        self.b_and_t_collision = False
        self._create_blocks(5)

    def _create_towers(self):
        """Create 3 towers at the center of screen"""
        pos_x, pos_y = self.screen_rect.centerx - 240, self.screen_rect.centery
        for i in range(0, 3):
            tower = Tower((pos_x, pos_y), i + 1)
            self.towers.append(tower)
            pos_x += 240

    def _create_blocks(self, quantity):
        """Create group of blocks"""
        width = 50 + (quantity * 10)

        for i in range(quantity, 0, -1):
            block = TowerBlock(width, 20, (0, 0), i)
            self.towers[0].add(block)
            self.blocks.append(block)
            width -= 10

    def run_game(self):
        """Method to Run Game"""
        # Main Game Loop
        while True:
            self._check_event()

            # Update setting screen assets
            if self.setting.display:
                self.setting.update()
                if self.setting.restart_flag:
                    self._restart_game()
                    self.setting.restart_flag = False
                    self.setting.display = False
            # Update main game assets
            else:
                self._update_main_assets()

            self._update_screen()

    def _check_event(self):
        """Check events and respond to them"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if self.setting.display:
                # Check Setting Screen Events
                self.setting.check_events(event)
            else:
                # Check Main Screen Events
                self._check_main_event(event)

    def _check_main_event(self, event):
        """Check Main Screen events"""
        # Keyboard Events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_ESCAPE:
                if self.setting.display:
                    self.setting.display = False
                else:
                    self.setting.display = True
        # Mouse Events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.b_and_t_collision = False
            mouse_pos = pygame.mouse.get_pos()
            block_clicked, self.moving_block = self._get_clicked_block(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.b_and_t_collision = True

    def _get_clicked_block(self, mouse_pos):
        """Get a block which is clicked if any"""
        block_clicked = False
        moving_block: TowerBlock | None = None
        for tower in self.towers:
            tower: Tower
            # if block_stack is empty skip check
            if len(tower.block_stack) == 0:
                continue
            # Only checks the first block in stack
            block: TowerBlock = tower.block_stack[0]
            block_clicked = block.rect.collidepoint(mouse_pos)
            if block_clicked:
                moving_block = block
                break

        return block_clicked, moving_block

    def _restart_game(self):
        """Restart the Game"""
        # Empty all Tower Stack
        for tower in self.towers:
            for i in range(0, len(tower.block_stack)):
                block = tower.block_stack.pop(0)
                block.belongs_to_stack = None   # THIS IS VERY, VERY IMPORTANT LINE
                # WITHOUT THIS BLOCK OVERLAPS EACH OTHER
                """
                Because if i don't write this, tower will assume that the block
                already belong to its stack, and end up not adding it in the stack.
                Then it assumes stack is empty and will add at the bottom of the stack
                """

        # Now add all block in first tower
        for block in self.blocks:
            block: TowerBlock
            self.towers[0].add(block)

    def _update_main_assets(self):
        """Update Main Screen Assets"""
        # Check the existence of moving block
        if self.moving_block:
            self.moving_block: TowerBlock | None
            # Move with the mouse pointer
            self.moving_block.update(pygame.mouse.get_pos())

            # If mouse button released check moving block collision with tower
            if self.b_and_t_collision:
                if not self._add_block_to_collided_tower():
                    self.moving_block.rect.center = self.moving_block.last_valid_position
                self.moving_block = None

    def _add_block_to_collided_tower(self):
        """Place block in a Tower"""
        # Check block collides with which tower
        for tower in self.towers:
            tower: Tower
            # If collides with tower add that block to that tower
            if tower.space_rect.collidepoint(self.moving_block.rect.center):
                tower.add(self.moving_block)
                return True
        return False

    def _update_screen(self):
        """Update images on screen and flip to new screen"""
        # Create Background
        self.screen.fill(self.setting.main_bg_color, self.screen_rect)

        # Create Towers
        for tower in self.towers:
            tower.draw_me(self.screen, self.setting.tower_color)

        # Draw Tower Blocks
        self._draw_blocks_on_screen()

        # Display Settings Screen if opened
        if self.setting.display:
            self.setting.blit_me(self.screen)

        # Update Display
        pygame.display.flip()

    def _draw_blocks_on_screen(self):
        """Draw Tower Block on Screen"""
        # Get the selected color from settings
        r, g, b = self.setting.tower_block_color
        for block in self.blocks:
            block: TowerBlock
            block.draw_me(self.screen, (r, g, b))
            # Make color of smaller blocks lighter
            r, g, b = r + 20, g + 20, b + 20


if __name__ == '__main__':
    toh = TowerOfHanoi()
    toh.run_game()
