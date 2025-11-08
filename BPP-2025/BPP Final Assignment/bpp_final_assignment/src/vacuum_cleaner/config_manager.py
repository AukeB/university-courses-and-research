"""Module for loading the configuration files."""

from ruamel.yaml import YAML  # type: ignore
from pathlib import Path
from pydantic import BaseModel, ConfigDict  # type: ignore


from src.vacuum_cleaner.utils import format_for_writing_to_yaml_file
from src.vacuum_cleaner.constants import CONFIG_PATH


yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)


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

    class Map(ConfiguredBaseModel):
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
    map: Map
    game: Game | None = None


class ConfigManager:
    def __init__(self, config_path: Path = CONFIG_PATH):
        self.config_path = config_path

    def load_config_file(self) -> ConfigModel:
        with open(self.config_path) as file:
            config = yaml.load(file)

        return ConfigModel(**config)

    def update_config_with_map_properties(
        self, config: ConfigModel, map: list[list[str]]
    ) -> ConfigModel:
        """
        Update config with map dimensions and max_steps.
        """
        rows = len(map)
        cols = len(map[0])

        updated_dimensions = ConfigModel.Map.Dimensions(columns=cols, rows=rows)

        # The total energy of the vacuum cleaner is always equal to two times the number of columns
        # times the number of rows.
        udpated_game = ConfigModel.Game(max_steps=2 * cols * rows)

        updated_map = config.map.copy(update={"dimensions": updated_dimensions})
        updated_config = config.copy(update={"map": updated_map, "game": udpated_game})

        return updated_config

    def export_config_to_yaml(self, config: ConfigModel) -> None:
        """ """
        config_dict = config.model_dump()

        config_formatted = format_for_writing_to_yaml_file(obj=config_dict)

        with open(Path("src/vacuum_cleaner/configs/config_map.yaml"), "w") as file:
            yaml.dump(config_formatted, file)
