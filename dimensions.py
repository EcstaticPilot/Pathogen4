from Observers.observer import Observable
import pygame, math

"""
Holds the mutable dimensions information about the window. updates as window resizes
"""

class Dimensions(Observable):

    def __init__(self):

        self.RATIO = 0.7

        self.FIELD_SIZE_IN_INCHES = 144
        self.FIELD_MARGIN_IN_PIXELS = 95 # the margin from image (0,0) to (0,0) of the field in pixels

        self.DEFAULT_SCREEN_WIDTH = 800
        self.DEFAULT_SCREEN_HEIGHT = 600

    def setFieldSizePixels(self, pixels: int):
        self.FIELD_SIZE_IN_PIXELS = pixels
        self.FIELD_SIZE_IN_PIXELS_NO_MARGIN = self.FIELD_SIZE_IN_PIXELS - 2 * self.FIELD_MARGIN_IN_PIXELS

    # Resize screen to (screenWidth, screenHeight) and return a new instance of the screen with updated dimensions
    def resizeScreen(self, screenWidth: int, screenHeight: int) -> pygame.Surface:


        self.SCREEN_WIDTH = screenWidth
        self.SCREEN_HEIGHT = screenHeight
        self.FIELD_WIDTH = int(screenWidth * self.RATIO)
        self.PANEL_WIDTH = screenWidth - self.FIELD_WIDTH

        ratioSquared = (self.SCREEN_WIDTH * self.SCREEN_HEIGHT) / (self.DEFAULT_SCREEN_HEIGHT * self.DEFAULT_SCREEN_WIDTH)
        self.RESOLUTION_RATIO = math.sqrt(ratioSquared)

        print(self.RESOLUTION_RATIO)

        larger = max(self.SCREEN_HEIGHT, self.FIELD_WIDTH)
        self.LARGER_FIELD_SIDE = larger

        screen = pygame.display.set_mode((screenWidth,screenHeight), pygame.RESIZABLE)
        self.notify()

        return screen
