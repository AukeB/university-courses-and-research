""" """

import pygame as pg # type: ignore

from src.vacuum_cleaner.map_loader import MapLoader
from src.vacuum_cleaner.config_manager import ConfigManager
from src.vacuum_cleaner.renderer import Renderer
from src.vacuum_cleaner.constants import ALL_PATHS


def main():
    """ """
    pg.init()

    for path in ALL_PATHS:
        # Load configuration file.
        config_manager = ConfigManager()
        config = config_manager.load_config_file()

        # Load map from the path to the .csv file.
        map_loader = MapLoader(path=path)
        map = map_loader.load_map()

        # Extent config settings with properties that can be extracted from the map.
        config = config_manager.update_config_with_map_properties(
            config=config,
            map=map
        )

        # Visualize the map
        renderer = Renderer(config=config, grid=map)
        renderer.visualize(display_time=3)

    pg.quit()

if __name__ == "__main__":
    main()