"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List
from random import random
from projects.pj02 import constants
from math import sin, cos, pi, sqrt


__author__ = "730233100"  # TODO


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)

    def distance(self, other: Point) -> float:
        """Calculates the distance between two points."""
        x_diff: float = (self.x - other.x) * (self.x - other.x)
        y_diff: float = (self.y - other.y) * (self.y - other.y)
        dist: float = (sqrt(x_diff + y_diff))
        return dist


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = 0

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    # Part 1) Define a method named `tick` with no parameters.
    # Its purpose is to reassign the object's location attribute
    # the result of adding the self object's location with its
    # direction. Hint: Look at the add method.
    def tick(self) -> None:
        """Performs one tick on a Cell object."""
        self.location = self.location.add(self.direction)
        if self.sickness >= constants.INFECTED:
            self.sickness += 1
            if self.sickness == constants.RECOVERY_PERIOD:
                self.immunize()
        
    def contract_disease(self) -> None:
        """Assign INFECTED to sickness."""
        self.sickness = constants.INFECTED

    def is_vulnerable(self) -> bool:
        """Returns True if the cell is vulnerable."""
        if self.sickness == constants.VULNERABLE:
            return True
        else:
            return False

    def is_infected(self) -> bool:
        """Returns True if the cell is vulnerable."""
        if self.sickness >= constants.INFECTED and self.sickness < constants.RECOVERY_PERIOD:
            return True
        else:
            return False

    def color(self) -> str:
        """Return the color representation sof a cell."""
        if self.is_vulnerable():
            return constants.CELL_COLOR
        if self.is_infected():
            return constants.CELL_COLOR_INFECTED
        if self.is_immune():
            return constants.CELL_COLOR_IMMUNE
        return constants.CELL_COLOR

    def contact_with(self, other: Cell) -> None:
        """Infects a vulnerable cell that comes in contact with an infected cell."""
        if self.is_vulnerable() and other.is_infected():
            self.contract_disease()
        if self.is_infected() and other.is_vulnerable():
            other.contract_disease()

    def immunize(self) -> None:
        """Immunizes a cell."""
        self.sickness = constants.IMMUNE

    def is_immune(self) -> bool:
        """Returns True if cell is immune."""
        if self.sickness == constants.IMMUNE:
            return True
        else:
            return False
    

class Model:
    """The state of the simulation."""

    population: List[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, infected: int, immune: int = 0):
        """Initialize the cells with random locations and directions."""
        self.population = []
        vulnerable: int = cells - infected - immune
        if infected >= cells:
            raise ValueError("Number of Infected cells must be less than number of total cells.")
        if infected <= 0:
            raise ValueError("Number of Infected cells must be greater than 0.")
        if immune >= cells:
            raise ValueError("Number of Immune cells must be less than number of total cells.")
        if immune < 0:
            raise ValueError("Number of Immune cells cannot be less than 0.")
        for _ in range(0, vulnerable):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            self.population.append(Cell(start_loc, start_dir))
        for _ in range(0, infected):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            infected_cell: Cell = Cell(start_loc, start_dir)
            infected_cell.contract_disease()
            self.population.append(infected_cell)
        for _ in range(0, immune):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            immune_cell: Cell = Cell(start_loc, start_dir)
            immune_cell.immunize()
            self.population.append(immune_cell)

    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
        self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        # TODO
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        # TODO
        random_angle = 2.0 * pi * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        infected: int = 0
        immune: int = 0
        vulnerable: int = 0
        for cell in self.population:
            if cell.is_vulnerable():
                vulnerable += 1
            if cell.is_immune():
                immune += 1
            if cell.is_infected():
                infected += 1
        if infected > 0:
            return False
        else:
            return True

    def check_contacts(self) -> None:
        """Method checking for contact of cells."""
        i: int = 0
        # for cell in self.population:
        #     comparison.append(cell)
        while i < len(self.population):
            j: int = 0
            if i == len(self.population) - 1:
                i = len(self.population)
                j = len(self.population)
            while j < len(self.population):
                if j <= i:
                    j = i + 1
                if self.population[j].location.distance(self.population[i].location) <= constants.CELL_RADIUS:
                    self.population[i].contact_with(self.population[j])
                j += 1
            i += 1