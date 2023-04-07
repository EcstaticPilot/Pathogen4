from entity_base.container_entity import Container
from entity_base.image.image_entity import ImageEntity

from common.draw_order import DrawOrder
from adapter.path_adapter import PathAdapter
from utility.pygame_functions import drawSurface
import pygame

"""
The command block icon should be placed at the left side of the command header
"""
class CommandBlockIcon(Container):

    def __init__(self, parentHeader, pathAdapter: PathAdapter):
        super().__init__(parent = parentHeader)
        self.pathAdapter = pathAdapter

        # Compute position BEFORE creating child entity
        self.recomputePosition()

        # ImageEntity is bounded exactly by the rect defined in this class
        self.image = ImageEntity(self, pathAdapter.getIcon(), drawOrder = DrawOrder.WIDGET, dimOnHover = False)

        # whenever path adapter updates, update icon
        pathAdapter.subscribe(onNotify = lambda: self.image.setImage(pathAdapter.getIcon()))

    def defineCenter(self) -> tuple:
        return self._ax(20), self._py(0.5)

    # must impl both of these if want to contain other entity
    def defineWidth(self) -> float:
        return self._pheight(0.8) # yes, this is height not width. square icon
    def defineHeight(self) -> float:
        return self._pheight(0.8)