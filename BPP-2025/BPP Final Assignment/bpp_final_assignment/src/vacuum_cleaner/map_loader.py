""" """

from pathlib import Path
import csv
from typing import List


class MapLoader:
    """Loads and parses a map from a CSV file."""

    def __init__(self, path: Path) -> None:
        """Initialize the MapLoader with a path to a CSV file."""
        self.path = path

    def load_map(self) -> List[List[str]]:
        """Load the CSV file (comma-delimited) and return its contents as a 2D list."""
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")

        with self.path.open(newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            data = [row for row in reader]

        if not data:
            raise ValueError(f"CSV file '{self.path}' is empty.")

        return data
