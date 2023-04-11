from __future__ import annotations
from typing import TYPE_CHECKING
from common.font_manager import FontID
from entity_base.container_entity import Container
from entity_base.listeners.hover_listener import HoverLambda
from entity_ui.dropdown.dropdown_container import DropdownContainer
from utility.pygame_functions import shade
if TYPE_CHECKING:
    from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity

from entity_base.entity import Entity
from entity_base.text_entity import TextEntity, TextAlign
from common.draw_order import DrawOrder
import pygame

"""
Draws the function name, and contains the dropdown to select the funciton
"""

class FunctionNameEntity(Entity):

    def __init__(self, parentHeader, parentCommand: CommandBlockEntity):
        
        self.parentCommand = parentCommand
        super().__init__(parent = parentHeader,
                         hover = HoverLambda(self),
                         drawOrder = DrawOrder.FUNCTION_NAME_BACKGROUND)
        
        self.dx = 19 # delta for text from left edge
        self.textEntity = None
        self.recomputePosition()

        self.CORNER_RADIUS = 5
        
        color = self.parentCommand.getColor()
        colorSelectedHovered = shade(color, 0.975)
        colorSelected = shade(color, 1)
        colorHovered = shade(color, 1.1)
        colorOff = shade(color, 1.3)
        
        self.dropdown = DropdownContainer(self, ["goForward()", "goForwardTimed()", "go()"],
                          FontID.FONT_NORMAL, 18,
                          colorSelectedHovered, colorSelected, colorHovered, colorOff,
                          dynamicWidth = True, dynamicBorderOpacity = True, centered = False,
                          iconScale = 0.6, textLeftOffset = 16, cornerRadius = 7, verticalTextPadding = 0)
        
        self.recomputePosition()

    def defineLeftX(self) -> tuple:
        return self._px(0) + self._pheight(1)
    
    def defineCenterY(self) -> float:
        return self._py(0.5)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:

        if self.textEntity is None:
            return 0

        RIGHT_MARGIN = 5
        return self._awidth(self.dx + RIGHT_MARGIN) + self.textEntity.getTextWidth() # yes, this is height not width. square icon
    
    def defineHeight(self) -> float:
        return self._pheight(0.8)
