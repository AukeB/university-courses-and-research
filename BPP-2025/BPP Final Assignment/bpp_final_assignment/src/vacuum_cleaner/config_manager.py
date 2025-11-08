"""Module for loading the configuration files."""

import yaml
from pathlib import Path
from pydantic import BaseModel, ConfigDict # type: ignore

from src.vacuum_cleaner.constants import CONFIG_PATH


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ConfigModel(ConfiguredBaseModel):
    """Config that combines all parameters"""

    class Window(ConfiguredBaseModel):
        width: int
        height: int
        title: str
        fps: int
        background_color: list[int]


    class Grid(ConfiguredBaseModel):
        
        class Dimensions(ConfiguredBaseModel):
            columns: int
            rows: int
        
        class Colors(ConfiguredBaseModel):

            wall: list[int]
            clean_floor: list[int]
            stain: list[int]
            vacuum_cleaner: list[int]
            grid_lines: list[int]

        margin: int
        colors: Colors
        dimensions: Dimensions | None = None
    
    class Game(ConfiguredBaseModel):
        max_steps: int | None = None

    window: Window
    grid: Grid
    game: Game | None = None


class ConfigManager:
    def __init__(self, config_path: Path = CONFIG_PATH):
        self.config_path = config_path

    def load_config_file(self) -> ConfigModel:
        with open(self.config_path) as file:
            config = yaml.safe_load(file)

        return ConfigModel(**config)
    
    def update_config_with_map_properties(
        self,
        config: ConfigModel,
        map: list[list[str]]
    ) -> ConfigModel:
        """
        Update config with map dimensions and max_steps.
        """
        rows = len(map)
        cols = len(map[0])

        new_dimensions = ConfigModel.Grid.Dimensions(columns=cols, rows=rows)
        new_game = ConfigModel.Game(max_steps=2*cols*rows)

        new_grid = config.grid.copy(update={"dimensions": new_dimensions})

        updated_config = config.copy(update={
            "grid": new_grid,
            "game": new_game
        })

        return updated_config