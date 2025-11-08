""" """

import pygame as pg # type: ignore

from src.vacuum_cleaner.map_loader import MapLoader
from src.vacuum_cleaner.renderer import Renderer
from src.vacuum_cleaner.constants import PATH_MAP_LVL_06_1, ALL_PATHS


def main():
    """ """
    pg.init()

    for path in ALL_PATHS:
        map_loader = MapLoader(path=path)
        map_data = map_loader.load_map()
        
        renderer = Renderer(grid=map_data)
        renderer.visualize(display_time=3)

    pg.quit()

if __name__ == "__main__":
    main()