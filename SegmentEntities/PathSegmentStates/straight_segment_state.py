from abc import ABC, abstractmethod
from enum import Enum
from reference_frame import PointRef, Ref

from SegmentEntities.path_segment_state import PathSegmentState
from SegmentEntities.edge_entity import EdgeEntity

from pygame_functions import drawLine
from math_functions import pointTouchingLine

import pygame

# Abstract class for a non-functional edge
# only purpose is to connect two points. 

class StraightSegmentState(PathSegmentState):
    def __init__(self, segment: EdgeEntity) -> None:
        super().__init__(segment)


    def isTouching(self, position: PointRef) -> bool:
        mx, my = position.screenRef
        x1, y1 = self.segment.first.getPosition().screenRef
        x2, y2 = self.segment.second.getPosition().screenRef
        return pointTouchingLine(mx, my, x1, y1, x2, y2, self.segment.hitboxThickness)

    def distanceTo(self, position: PointRef) -> float:
        return (self.getPosition() - position).magnitude(Ref.SCREEN)

    def getPosition(self) -> PointRef:
        fpos = self.segment.first.getPosition()
        spos = self.segment.second.getPosition()

        return fpos + (spos - fpos) / 2

    def draw(self, screen: pygame.Surface, isActive: bool, isHovered: bool) -> bool:
        
        x1, y1 = self.segment.first.getPosition().screenRef
        x2, y2 = self.segment.second.getPosition().screenRef

        drawLine(screen, self.segment.getColor(isActive, isHovered), x1, y1, x2, y2, self.segment.thickness, None)

    def toString(self) -> str:
        return "straight"