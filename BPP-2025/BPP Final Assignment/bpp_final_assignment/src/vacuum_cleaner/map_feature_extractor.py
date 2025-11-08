""" """


class MapFeatureExtractor:
    """ """

    def __init__(self, map: list[list[str]]) -> None:
        """ """
        self.map = map
        self.stain_size: int = self._determine_stain_size()

    def _determine_stain_size(self) -> int:
        """
        Determine the size of a square stain (@) in a map.
        Assumes all stains are square and contiguous.

        Returns:
            size of the square (number of cells along one side)
        """
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == "@":
                    width = 0
                    while x + width < len(row) and row[x + width] == "@":
                        width += 1

                    # Count vertical length
                    height = 0
                    while y + height < len(self.map) and self.map[y + height][x] == "@":
                        height += 1

                    if width != height:
                        raise ValueError(
                            f"Stain at ({x},{y}) is not square: {width}x{height}"
                        )

                    return width

        raise ValueError("No stain found in the map")
