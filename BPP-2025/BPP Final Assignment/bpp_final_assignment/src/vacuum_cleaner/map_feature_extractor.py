""" """


class MapFeatureExtractor:
    """ """

    def __init__(self, map: list[list[str]]) -> None:
        """ """
        self.map = map

        self.number_of_rows = len(self.map)
        self.number_of_columns = len(self.map[0])
        self.max_steps = 2 * self.number_of_rows * self.number_of_columns

        self.stain_size: int = self._determine_object_size(cell_value="@")
        self.number_of_stains: int = self._determine_number_of_objects(
            object_size=self.stain_size, cell_value="@"
        )

    def _determine_object_size(self, cell_value: str) -> int:
        """ """

        def find_distance_to_different_neighbor(
            y: int, x: int, dy: int, dx: int, cell_value: str
        ) -> int:
            """ """
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
                if cell == cell_value:
                    width = (
                        1
                        + find_distance_to_different_neighbor(y, x, 0, -1, cell_value)
                        + find_distance_to_different_neighbor(y, x, 0, 1, cell_value)
                    )
                    height = (
                        1
                        + find_distance_to_different_neighbor(y, x, -1, 0, cell_value)
                        + find_distance_to_different_neighbor(y, x, 1, 0, cell_value)
                    )

                    widths.append(width)
                    heights.append(height)

        if not widths or not heights:
            raise ValueError("No objects found in the map")

        width_value = min(widths)
        height_value = min(heights)

        if width_value != height_value:
            raise ValueError(
                f"Inconsistent object shape: width={width_value}, height={height_value}"
            )

        return width_value

    def _determine_number_of_objects(self, object_size: int, cell_value: str) -> int:
        """ """
        count = 0

        for y in range(self.number_of_rows - object_size + 1):
            for x in range(self.number_of_columns - object_size + 1):
                full_object = True

                for dy in range(object_size):
                    for dx in range(object_size):
                        if self.map[y + dy][x + dx] != cell_value:
                            full_object = False
                            break
                    if not full_object:
                        break

                if full_object:
                    count += 1

        return count
