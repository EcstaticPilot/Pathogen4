from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from BaseEntity.EntityFunctions.click_function import Click
from BaseEntity.EntityFunctions.drag_function import Drag
from BaseEntity.EntityFunctions.select_function import Select
from BaseEntity.EntityFunctions.tick_function import Tick

import pygame

class Entity(ABC):

    # drawOrder is a number, in which the lowest number is drawn in the front (highest number is drawn first)
    def __init__(self, drag: Drag = None, select: Select = None, click: Click = None, tick: Tick = None, drawOrder: int = 0) -> None:
        self.drawOrder = drawOrder
        self.drag = drag
        self.select = select
        self.click = click
        self.tick = tick
        self.children: list[Entity] = []
    
    def addChild(self, child: 'Entity'):
        self.children.append(child)
        
    @abstractmethod
    def isVisible(self) -> bool:
        pass

    @abstractmethod
    def isTouching(self, position: PointRef) -> bool:
        pass

    def distanceTo(self, position: PointRef) -> float:
        return (position - self.getPosition()).magnitude(Ref.SCREEN)

    @abstractmethod
    def getPosition(self) -> PointRef:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        pass

    @abstractmethod
    def toString(self) -> str:
        pass

    def __str__(self):
        return f"Entity: {self.toString()}"
