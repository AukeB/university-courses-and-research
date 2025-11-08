""" """

import pygame as pg  # type: ignore

from src.vacuum_cleaner.config_manager import ConfigModel


class Renderer:
    """Handles window setup and visualization for the simulation."""

    def __init__(self, config: ConfigModel, grid: list[list[str]]) -> None:
        """Initialize display and simulation timing."""
        self.grid = grid

        # Window setup
        self.screen_width = config.window.width
        self.screen_height = config.window.height
        self.window_title = config.window.title
        self.fps = config.window.fps
        self.background_color = config.window.background_color

        # Grid related
        self.grid_dimensions_columns = config.map.dimensions.columns
        self.grid_dimensions_rows = config.map.dimensions.rows
        self.grid_lines_color = config.map.colors.grid_lines

        # Define grid drawing area (smaller than the full window)
        self.margin = config.map.margin  # Unit: pixels.
        self.grid_width = self.screen_width - 2 * self.margin
        self.grid_height = self.screen_height - 2 * self.margin

        # Compute cell size to fit grid within grid_area
        self.cell_width = self.grid_width / self.grid_dimensions_columns
        self.cell_height = self.grid_height / self.grid_dimensions_rows

        # Correct them for when 'cell_width' and 'cell_height' are not integers.
        self._readjust_size_parameters()

        # Offset to center the grid
        self.offset_x = self.margin
        self.offset_y = self.margin

        # Initialize Pygame
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption(self.window_title)

        self.time_elapsed = 0.0

        # Color map for each symbol
        self.color_mapping = {
            "x": config.map.colors.wall,
            ".": config.map.colors.clean_floor,
            "@": config.map.colors.stain,
            "#": config.map.colors.vacuum_cleaner,
        }

    def _readjust_size_parameters(self) -> None:
        """ """
        self.cell_width, self.cell_height = int(self.cell_width), int(self.cell_height)

        self.grid_width = self.cell_width * self.grid_dimensions_columns
        self.grid_height = self.cell_height * self.grid_dimensions_rows

        self.screen_width = self.grid_width + 2 * self.margin
        self.screen_height = self.grid_height + 2 * self.margin

    def visualize(self, display_time: float | None = None) -> None:
        """
        Main render loop for the simulation.

        Args:
            display_time: If given, automatically stops after this many seconds.
        """
        self.time_elapsed = 0.0
        running = True

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            dt = self.clock.get_time() / 1000.0
            self.time_elapsed += dt

            self.screen.fill(self.background_color)
            self._draw_grid()

            pg.display.flip()
            self.clock.tick(self.fps)

            if display_time is not None and self.time_elapsed >= display_time:
                running = False

    def _draw_grid(self) -> None:
        """
        Draw all cells from the grid.
        """
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                color = self.color_mapping.get(cell, (255, 0, 0))  # Use red if unknown.

                rect = pg.Rect(
                    self.offset_x + x * self.cell_width,
                    self.offset_y + y * self.cell_height,
                    self.cell_width,
                    self.cell_height,
                )

                pg.draw.rect(self.screen, color, rect)
                pg.draw.rect(self.screen, self.grid_lines_color, rect, 1)
