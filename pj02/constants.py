"""Constants used through the simulation."""

BOUNDS_WIDTH: int = 400
MAX_X: float = BOUNDS_WIDTH / 2
MIN_X: float = -MAX_X
VIEW_WIDTH: int = BOUNDS_WIDTH + 20

BOUNDS_HEIGHT: int = 400
MAX_Y: float = BOUNDS_HEIGHT / 2
MIN_Y: float = -MAX_Y
VIEW_HEIGHT: int = BOUNDS_HEIGHT + 20

CELL_RADIUS: int = 15
CELL_COUNT: int = 10
CELL_COUNT_INFECTED: int = 1
CELL_COUNT_IMMUNE: int = 0
CELL_SPEED: float = 5.0
CELL_COLOR: str = "gray"
CELL_COLOR_INFECTED: str = "red"
CELL_COLOR_IMMUNE: str = "purple"

INFECTED: int = 1
VULNERABLE: int = 0
IMMUNE: int = -1

RECOVERY_PERIOD: int = 90