class Battlefield:
    # map_array
    matrix: list[list[str]]
    points: list[tuple[int, int]]

    def __init__(self, height: int, width: int, matrix=[]):
        self.battlefield = matrix
        self.width = width
        self.height = height
        self.points = []

    # The selected states should be within the battlefield area...
    def check_out(self, y: int, x: int) -> bool:
        return x >= self.width or x < 0 or y >= self.height or y < 0

    # This function detects barriers in the battlefield:
    def is_barrier(self, y: int, x: int):
        return self.battlefield[y][x].lower() == "x"

    def set_points(self, points):
        self.points = points

    def get_state(self, y, x) -> str:
        return self.battlefield[y][x]

    def append_row(self, row: list[str]) -> None:
        if len(row) != self.width:
            raise ValueError("Invalid size of columns in this row:\n", str(row))
        self.battlefield.append(row)
