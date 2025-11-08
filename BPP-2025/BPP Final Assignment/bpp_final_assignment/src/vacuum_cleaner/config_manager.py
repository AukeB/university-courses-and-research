"""Module for loading the configuration files."""

from ruamel.yaml import YAML  # type: ignore
from pathlib import Path
from pydantic import BaseModel, ConfigDict  # type: ignore


from src.vacuum_cleaner.map_feature_extractor import MapFeatureExtractor
from src.vacuum_cleaner.utils import format_for_writing_to_yaml_file
from src.vacuum_cleaner.constants import CONFIG_PATH, CONFIG_MAP_OUTPUT_PATH


yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ConfigModel(ConfiguredBaseModel):
    """Config that combines all parameters"""

    class Window(ConfiguredBaseModel):
        title: str
        width: int
        height: int
        margin: int
        fps: int
        background_color: list[int]

    class Map(ConfiguredBaseModel):
        class Colors(ConfiguredBaseModel):
            wall: list[int]
            clean_floor: list[int]
            stain: list[int]
            vacuum_cleaner: list[int]
            grid_lines: list[int]

        class Dimensions(ConfiguredBaseModel):
            columns: int
            rows: int

        class ObjectProperties(ConfiguredBaseModel):
            stain_size: int
            number_of_stains: int

        colors: Colors
        dimensions: Dimensions | None = None
        object_properties: ObjectProperties | None = None

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
        # Extract features from map with custom logic.
        map_feature_extractor = MapFeatureExtractor(map=map)

        # Create ConfigModel objects for new/updated parameters.
        updated_dimensions = ConfigModel.Map.Dimensions(
            columns=map_feature_extractor.number_of_columns,
            rows=map_feature_extractor.number_of_rows,
        )

        updated_game = ConfigModel.Game(max_steps=map_feature_extractor.max_steps)

        object_properties = ConfigModel.Map.ObjectProperties(
            stain_size=map_feature_extractor.stain_size,
            number_of_stains=map_feature_extractor.number_of_stains,
        )

        # Update configuration variable.
        updated_map = config.map.copy(
            update={
                "dimensions": updated_dimensions,
                "object_properties": object_properties,
            }
        )

        updated_config = config.copy(update={"map": updated_map, "game": updated_game})

        return updated_config

    def export_config_to_yaml(self, config: ConfigModel) -> None:
        """ """
        config_dict = config.model_dump()
        config_formatted = format_for_writing_to_yaml_file(obj=config_dict)

        with open(CONFIG_MAP_OUTPUT_PATH, "w") as file:
            yaml.dump(config_formatted, file)
