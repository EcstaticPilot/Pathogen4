from reference_frame import PointRef

from BaseEntity.entity import Entity

import pygame

"""
A entity that does not change and is always drawn
Not subclassable.
Pass a lambda function that draws the thing you want to the constructor.
EntityManager will automatically draw that thing every frame, respecting drawOrder
"""
class StaticEntity(Entity):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, Fdraw = lambda: None, Ftouching = lambda position: False, drawOrder: int = 0, name: str = "Static Entity") -> None:
        super().__init__(drawOrder = drawOrder)
        self.Fdraw = Fdraw
        self.Ftouching = Ftouching
        self.name = name
        
    def isVisible(self) -> bool:
        return True

    def isTouching(self, position: PointRef) -> bool:
        return self.Ftouching(position)

    def getPosition(self) -> PointRef:
        return PointRef()

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        self.Fdraw()

    def toString(self) -> str:
        return self.name