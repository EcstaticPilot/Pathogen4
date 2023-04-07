from entity_base.container_entity import Container
from entity_base.entity import Entity
from entity_ui.group.linear_container import LinearContainer
from typing import TypeVar, Generic

from entity_ui.group.linear_group_container import LinearGroupContainer

"""
A LinearGroupContainer that expands dynamically as more entities are added.
Specifically, it has a fixed individual entity size, so adding an entity
grows the group by that much.
It is top-left aligned with parent rect, but can grow below/right of the parent bounds
"""
T = TypeVar('T')
class DynamicGroupContainer(LinearGroupContainer['T']):

    def __init__(self, parent: Entity, isHorizontal: bool, entitySizePixels: float):
        
        super().__init__(parent, isHorizontal)

        self.pixels = entitySizePixels
        self.groupSize = 0

        self.recomputePosition()

    # add linear entity to group. returns the linear entity's location
    def add(self, entity: LinearContainer):
        super().add(entity)
        self.groupSize += self.pixels

    def defineWidth(self) -> float:
        if self.isHorizontal:
            return self._pwidth(1)
        else:
            return self._awidth(self.pixels)
        
    def defineHeight(self) -> float:
        if self.isHorizontal:
            return self._aheight(self.groupSize)
        else:
            return self._pheight(1)
        
    def defineTopLeft(self) -> tuple:
        return self._px(0), self._py(0)
