""" """

import pygame as pg # type: ignore

from src.vacuum_cleaner.map_loader import MapLoader
from src.vacuum_cleaner.config_manager import ConfigManager
from src.vacuum_cleaner.renderer import Renderer
from src.vacuum_cleaner.constants import ALL_PATHS

from pathlib import Path

def main():
    """ """
    pg.init()

    for path in ALL_PATHS:
        # if path == Path("src/vacuum_cleaner/maps/map_lvl_10_3.csv"):
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

        # Export config after it was updated for clarity.
        config_manager.export_config_to_yaml(config=config)

        # Visualize the map
        renderer = Renderer(config=config, grid=map)
        renderer.visualize(display_time=0.5)

    pg.quit()

if __name__ == "__main__":
    main()