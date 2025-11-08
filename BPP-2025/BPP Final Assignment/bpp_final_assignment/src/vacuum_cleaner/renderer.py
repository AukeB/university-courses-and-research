""" """

import pygame as pg # type: ignore


class Renderer:
    """Handles window setup and visualization for the simulation."""

    def __init__(
        self,
        grid: list[list[str]]
    ) -> None:
        """Initialize display and simulation timing."""
        self.grid = grid

        # Window setup
        self.screen_width = 2400
        self.screen_height = 2400
        self.window_title = "Vacuum Cleaner Simulation"
        self.fps = 60

        # Grid dimensions
        self.grid_dimensions_width = len(self.grid[0])
        self.grid_dimensions_height = len(self.grid)

        # Define grid drawing area (smaller than the full window)
        self.margin = 100  # Unit: pixels.
        self.grid_width = self.screen_width - 2 * self.margin
        self.grid_height = self.screen_height - 2 * self.margin

        # Compute cell size to fit grid within grid_area
        self.cell_width = self.grid_width / self.grid_dimensions_width
        self.cell_height = self.grid_height / self.grid_dimensions_height

        # Correct them for when 'cell_width' and 'cell_height' are not integers.
        self._readjust_size_parameters()

        # Offset to center the grid
        self.offset_x = self.margin
        self.offset_y = self.margin

        # Initialize Pygame
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pg.display.set_caption(self.window_title)

        self.time_elapsed = 0.0

        # Color map for each symbol
        self.colors = {
            "x": (255, 255, 255),    # Walls (white)
            ".": (205, 170, 125),    # Clean floor (light brown, parquet-like)
            "@": (139, 69, 19),      # Stain (dark brown)
            "#": (0, 0, 0),          # Starting square / vacuum (black)
        }
    
    def _readjust_size_parameters(self) -> None:
        """ """
        self.cell_width, self.cell_height = int(self.cell_width), int(self.cell_height)

        self.grid_width = self.cell_width * self.grid_dimensions_width
        self.grid_height = self.cell_height * self.grid_dimensions_height

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

            self.screen.fill((0, 0, 0))
            self._draw_grid()

            pg.display.flip()
            self.clock.tick(self.fps)

            if display_time is not None and self.time_elapsed >= display_time:
                running = False

    def _draw_grid(self) -> None:
        """Draw all cells from the grid."""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                color = self.colors.get(cell, (255, 0, 0))  # Use red if unknown.
                rect = pg.Rect(
                    self.offset_x + x * self.cell_width,
                    self.offset_y + y * self.cell_height,
                    self.cell_width,
                    self.cell_height
                )

                pg.draw.rect(self.screen, color, rect)
                # Draw black grid lines
                pg.draw.rect(self.screen, (0, 0, 0), rect, 1)
