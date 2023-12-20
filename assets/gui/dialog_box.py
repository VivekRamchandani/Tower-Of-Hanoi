import pygame

from .blocks import ColorBlock


class DialogBox:
    """Create and manage Dialog Box"""
    def __init__(self, width, height, position):

        # Creating Box Rectangle and Setting its position
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = position

        self.options_width = width - 40
        self.options_height = int((height - 60) / 2)

        # Font properties
        self.font = pygame.font.Font('./assets/fonts/TisaSansPro-Bold.ttf', 22)
        self.font_color = (80, 80, 80)

        # Prepare Option space
        self._prep_options()

        # Prepare Texts
        self._prep_texts()

        # Prepare Color Blocks
        self._prep_block_color_blocks()
        self._prep_bg_color_blocks()

    def _prep_options(self):
        """Prepare Option Space"""
        # Option 1
        option1_rect = pygame.Rect(0, 0, self.options_width, self.options_height)
        option1_rect.x, option1_rect.y = self.rect.x + 20, self.rect.y + 20

        # Option 2
        option2_rect = pygame.Rect(0, 0, self.options_width, self.options_height)
        option2_rect.x, option2_rect.y = self.rect.x + 20, self.rect.y + self.options_height + 40

        # Grouping options
        self.options = [option1_rect, option2_rect]

    def _prep_texts(self):
        """Prepare text in options"""
        self.opt1_txt_img = self.font.render("Background Color", True, self.font_color, None)
        self.opt1_txt_img_rect = self.opt1_txt_img.get_rect()
        self.opt1_txt_img_rect.x, self.opt1_txt_img_rect.y = self.options[0].x, self.options[0].y

        self.opt2_txt_img = self.font.render("Block Color", True, self.font_color, None)
        self.opt2_txt_img_rect = self.opt2_txt_img.get_rect()
        self.opt2_txt_img_rect.x, self.opt2_txt_img_rect.y = self.options[1].x, self.options[1].y

    def _prep_block_color_blocks(self):
        """Prepare Color Blocks for Blocks"""
        self.block_color_blocks: list[ColorBlock] = []
        colors = [(170, 80, 80), (80, 170, 80), (80, 80, 170)]
        width = int((self.options_width - 30) / 3)
        height = 25
        x, y = self.options[1].x, self.options[1].y + 32
        for color in colors:
            color_block = ColorBlock(width, height, color, (x, y))
            self.block_color_blocks.append(color_block)
            x += width + 10

    def _prep_bg_color_blocks(self):
        """Prepare Color Blocks for Background"""
        self.bg_color_blocks: list[ColorBlock] = []
        colors = [(255, 255, 255), (60, 60, 60)]
        width = int((self.options_width - 30) / 3)
        height = 25
        x, y = self.options[0].x, self.options[0].y + 32
        for color in colors:
            color_block = ColorBlock(width, height, color, (x, y))
            self.bg_color_blocks.append(color_block)
            x += width + 10

    def draw_me(self, surface: pygame.Surface):
        """Draw the whole Dialog Box and its components"""
        # The main Box
        pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=12)

        # Option Space
        for option_rect in self.options:
            pygame.draw.rect(surface, (255, 255, 255), option_rect, border_radius=12)

        # Option Texts
        surface.blit(self.opt1_txt_img, self.opt1_txt_img_rect)
        surface.blit(self.opt2_txt_img, self.opt2_txt_img_rect)

        # Background Color Blocks
        for color_block in self.bg_color_blocks:
            color_block.draw_me(surface)

        # Block Color Blocks
        for color_block in self.block_color_blocks:
            color_block.selected = False
            color_block.draw_me(surface)
