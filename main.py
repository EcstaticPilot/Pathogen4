from entity_base.entity import Entity
from entity_base.static_entity import StaticEntity
from entity_base.entity import initEntityClass, setRootContainer
from entity_ui.dropdown.dropdown_container import DropdownContainer
from entity_ui.group.variable_group.variable_container import VariableContainer
from entity_ui.group.variable_group.variable_group_container import VariableGroupContainer
from entity_ui.selector_menu.selector_menu_manager import SelectorMenuManager
from models.command_models.full_model import FullModel

from root_container.field_container.node.path_node_entity import PathNodeEntity
from root_container.field_container.segment.path_segment_entity import PathSegmentEntity
from root_container.panel_container.command_block.command_block_entity import CommandBlockEntity
from root_container.panel_container.command_block.command_inserter import CommandInserter

from root_container.panel_container.tab.tab_handler import TabHandler

from entity_handler.entity_manager import EntityManager
from entity_handler.interactor import Interactor

from root_container.path import Path

from command_creation.command_definition_database import CommandDefinitionDatabase
from command_creation.test_commands import *
from command_creation.command_block_entity_factory import CommandBlockEntityFactory

from root_container.panel_container.command_expansion.command_expansion_container import CommandExpansionContainer

from root_container.panel_container.panel_container import PanelContainer
from root_container.field_container.field_container import FieldContainer

from root_container.panel_container.command_scrolling.command_scrollbar import CommandScrollbar

from entity_ui.tooltip import initTooltipFont

from common.font_manager import FontManager, FontID
from common.image_manager import ImageManager, ImageID
from common.reference_frame import PointRef, Ref, initReferenceframe, VectorRef
from common.field_transform import FieldTransform
from common.dimensions import Dimensions
from common.draw_order import DrawOrder
from utility.pygame_functions import getGradientSurface
from utility.math_functions import isInsideBox2
import pygame, random, threading, time, json
import sys

import cProfile


pygame.init()
pygame.key.set_repeat(400, 70)

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]

def instanceOfClasses(entity, *classes):
    for c in classes:
        if isinstance(entity, c):
            return True
    return False

# Define the I/O handling function
def io_handler(database: CommandDefinitionDatabase, model: FullModel, entities: EntityManager):
    while True:
        cmd = input("Enter some text: ")
        
        if cmd == "json":
            commandJSON: dict = database.exportToJson()
            print(json.dumps(commandJSON, indent = 4))
        elif cmd == "model":
            model.tree()
        elif cmd == "ui":
            model.getExistingUI().tree(verbose=False)
        elif cmd == "cmd":
            print([e for e in entities.entities if isinstance(e, CommandBlockEntity)])

def main():

    # Initialize field
    dimensions = Dimensions()
    fontManager = FontManager(dimensions)
    screen = dimensions.resizeScreen(dimensions.DEFAULT_SCREEN_WIDTH, dimensions.DEFAULT_SCREEN_HEIGHT)

    images = ImageManager()
    imageSize = images.get(ImageID.FIELD).get_width()
    dimensions.setFieldSizePixels(imageSize)


    fieldTransform: FieldTransform = FieldTransform(images, dimensions)
    initReferenceframe(dimensions, fieldTransform)
    
    initTooltipFont(fontManager.getDynamicFont(FontID.FONT_NORMAL, 10))
    
    # Initialize entities
    interactor = Interactor(dimensions, fieldTransform)
    entities = EntityManager()
    initEntityClass(entities, interactor, images, fontManager, dimensions, fieldTransform)
    rootContainer = entities.initRootContainer()
    setRootContainer(rootContainer)

    # Add permanent static entities
    panelContainer = PanelContainer()
    fieldContainer = FieldContainer(fieldTransform)

    # handles the creating of menus when an entity is selected
    menuManager = SelectorMenuManager(fieldContainer)
    interactor.initInteractor(menuManager, fieldContainer)

    

    StaticEntity(lambda: interactor.drawSelectBox(screen), drawOrder = DrawOrder.MOUSE_SELECT_BOX)

    # initialize commands
    database = CommandDefinitionDatabase()

    # create tabs
    tabHandler = TabHandler(panelContainer, database)

    # create command model
    model = FullModel(tabHandler.blockContainer)

    # Create path
    path = Path(fieldContainer, tabHandler.blockContainer, model, database, PointRef(Ref.FIELD, (24,24)))
    fieldContainer.initPath(path)

    # initialize pygame artifacts
    pygame.display.set_caption("Pathogen 4.0 (Ansel Chang)")
    clock = pygame.time.Clock()

    # initialize everything
    print(model.tree())
    print(model.ui.tree())
    print("compute everything")
    rootContainer.recomputeEntity()

    # Create a new thread for the I/O handling function
    io_thread = threading.Thread(target=io_handler, args = (database,model,entities,), daemon=True)

    # Start the I/O handling thread
    io_thread.start()

    # Main game loop
    print("start loop")
    while True:

        dimensions.RESIZED_THIS_FRAME = False

        mouse = pygame.mouse.get_pos()
        

        mouseRef = PointRef(Ref.SCREEN, mouse)
        hoveredEntity = entities.getEntityAtPosition(mouse)

        if hoveredEntity is not None:
            parent = f", {str(hoveredEntity._parent)}"
        else:
            parent = ""
        pygame.display.set_caption(f"({mouse[0]}, {mouse[1]}), {str(hoveredEntity)}" + parent)

        interactor.setHoveredEntity(hoveredEntity, mouse)
        # handle events and call callbacks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = dimensions.resizeScreen(*event.size)
                fieldTransform.resizeScreen()
            elif event.type == pygame.MOUSEWHEEL and mouse[0] < dimensions.FIELD_WIDTH:
                fieldTransform.changeZoom(mouseRef, event.y * 0.01)
            elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
                ctrlKey = pygame.key.get_pressed()[pygame.K_LCTRL]
                shiftKey = pygame.key.get_pressed()[pygame.K_LSHIFT]
                right = (event.button == 1 and ctrlKey) or event.button == 3
                interactor.onMouseDown(entities, mouse, right, shiftKey)

            elif event.type == pygame.MOUSEBUTTONUP:
                interactor.onMouseUp(entities, mouse)

            elif event.type == pygame.MOUSEMOTION:
                interactor.onMouseMove(entities, mouse)
            elif event.type == pygame.KEYDOWN:
                entities.onKeyDown(event.key)
            elif event.type == pygame.KEYUP:
                entities.onKeyUp(event.key)

        # Perform calculations
        entities.tick()

        # Draw everything
        entities.drawEntities(interactor, screen, mouse, dimensions)

        # Update display and maintain frame rate
        pygame.display.flip()
        clock.tick(60) # fps
        #print(clock.get_fps())

if __name__ == "__main__":
    #cProfile.run('main()', sort='cumtime')
    main()
