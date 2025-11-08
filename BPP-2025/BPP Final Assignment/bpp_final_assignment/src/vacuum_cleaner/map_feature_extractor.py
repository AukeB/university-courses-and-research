""" """


class MapFeatureExtractor:
    """ """

    def __init__(self, map: list[list[str]]) -> None:
        """ """
        self.map = map

        self.number_of_rows = len(self.map)
        self.number_of_columns = len(self.map[0])
        self.max_steps = 2 * self.number_of_rows * self.number_of_columns
        self.stain_size: int = self._determine_stain_size()

    def _determine_stain_size(self) -> int:
        """
        Determine the size of a square stain (@) in a map.
        Assumes all stains are square and contiguous, but can handle
        multiple stains or adjacent stains by taking the most common
        width and height found among all '@' cells.

        Returns:
            size of the square (number of cells along one side)
        """

        def find_distance_to_different_neighbor(
            y: int, x: int, dy: int, dx: int, cell_value: str
        ) -> int:
            distance = 0

            while (
                0 <= y + (distance + 1) * dy < len(self.map)
                and 0 <= x + (distance + 1) * dx < len(self.map[y])
                and self.map[y + (distance + 1) * dy][x + (distance + 1) * dx]
                == cell_value
            ):
                distance += 1

            return distance

        widths = []
        heights = []

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == "@":
                    width = (
                        1
                        + find_distance_to_different_neighbor(y, x, 0, -1, "@")
                        + find_distance_to_different_neighbor(y, x, 0, 1, "@")
                    )
                    height = (
                        1
                        + find_distance_to_different_neighbor(y, x, -1, 0, "@")
                        + find_distance_to_different_neighbor(y, x, 1, 0, "@")
                    )

                    widths.append(width)
                    heights.append(height)

        if not widths or not heights:
            raise ValueError("No stain found in the map")

        width_value = min(widths)
        height_value = min(heights)

        if width_value != height_value:
            raise ValueError(
                f"Inconsistent stain shape: most common width={width_value}, "
                f"height={height_value}"
            )

        return width_value
