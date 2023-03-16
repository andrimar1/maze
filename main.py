#!/usr/bin/env python3

from typing import List, Dict
import argparse
import sys
import re

def read_input(input_file: str) -> List:
    """ Read and parse input file containing game def"""
    with open(input_file, 'r') as file:
        data = file.read()
    return parse_input(data)

def clean_str(strings: str) -> List:
    """Split strings on newline and strip empty elements"""
    return [x for x in strings.split("\n") if x]

def parse_input(data: List) -> Dict:
    """Parse game specifications from input data"""
    data = [clean_str(item) for item in data.split("-1")]
    d = {
        "board_dimension": [int(item) for item in data[0][0].split(",")],
        "mirrors": [parse_posdir(mirror) for mirror in data[1]],
        "laser_input": parse_posdir(data[2][0])
    }
    return d

def parse_posdir(posdir: str) -> Dict:
    """"Split string containing position and direction and return as dictionary"""
    parts = re.search("^(\d+),(\d+)([A-Z]{1,2})$", posdir)
    info = {
        "position": [int(parts.group(1)), int(parts.group(2))],
        "direction": parts.group(3)
    }
    return info

GAME_NAME = "Mirror House"
MAX_STEPS = 2000

class MirrorRoom:
    """
    Class that contains mirror information
    """

    def __init__(self, mirror_info: Dict) -> None:
        self.position = mirror_info.get("position")
        self.mirror_info = mirror_info
        self.lean = mirror_info.get("direction")[0]

        if len(self.mirror_info.get("direction")) == 2:
            self.reflect_dir = mirror_info.get("direction")[1]
        else:
            self.reflect_dir = "DUAL"

    def get_output_dir(self, input_dir: str) -> str:
        """
        Class method for checking whether and if so in which direction laser beam is reflected
        of mirror based on input direction of leaser, lean of mirror and reflection direction
        """
        # Case laser input direction is UP
        if input_dir == "UP":
            if self.lean == "L" and self.reflect_dir in ["DUAL", "L"]:
                return "LEFT"
            if self.lean == "R" and self.reflect_dir in ["DUAL", "R"]:
                return "RIGHT"

        # Case laser input direction is Down
        elif input_dir == "DOWN":
            if self.lean == "L" and self.reflect_dir in ["DUAL", "R"]:
                return "RIGHT"
            if self.lean == "R" and self.reflect_dir in ["DUAL", "L"]:
                return "LEFT"

        # Case laser input direction is Right
        elif input_dir == "RIGHT":
            if self.lean == "L" and self.reflect_dir in ["DUAL", "L"]:
                return "DOWN"
            if self.lean == "R" and self.reflect_dir in ["DUAL", "L"]:
                return "UP"

        # Case laser input direction is Left
        elif input_dir == "LEFT":
            if self.lean == "L" and self.reflect_dir in ["DUAL", "R"]:
                return "UP"
            if self.lean == "R" and self.reflect_dir in ["DUAL", "R"]:
                return "DOWN"

        return input_dir


class Board:
    """
    Board definition
    """

    def __init__(self, board_dimensions: list, mirrors: list) -> None:
        self.dim = board_dimensions
        self.mirror_rooms = []

        for mirror in mirrors:
            self.mirror_rooms.append(MirrorRoom(mirror))

    def print_board_info(self) -> None:
        """ Print board details"""
        print(":: Board dimensions: {0} by {1}, ".format(self.dim[0], self.dim[1]))
        print(":: Mirror count: {0}, ".format(len(self.mirror_rooms)))


class Game:
    """
    Game Definition
    """

    def __init__(self, board_dimensions: List, mirrors: List[Dict], laser_entry: Dict) -> None:
        self.board = Board(board_dimensions, mirrors)

        # Initialize laser position and direction
        self.laser_entry = laser_entry
        self.x = laser_entry.get("position")[0]
        self.y = laser_entry.get("position")[1]
        self.direction = self.laser_start_dir(laser_entry)

        # Log steps
        self.steps = 0
        self.last_step = {}

        # Print Game info
        self.board.print_board_info()
        self.print_laser_info()

    def print_laser_info(self):
        """ Print laser info """
        dir = "V" if self.direction in ["UP", "DOWN"] else "H"
        print(":: Laser start pos : {}, direction: {}, ".format(self.laser_entry.get("position"), dir))


    def laser_start_dir(self, laser_entry: Dict) -> str:
        """Find laser direction based on laser position and the boarders of board"""
        laser_position = laser_entry.get("position")
        if laser_position[0] == 0:
            return "RIGHT"
        elif laser_position[0] == self.board.dim[0]:
            return "LEFT"
        elif laser_position[1] == 0:
            return "UP"
        elif laser_position[1] == self.board.dim[1]:
            return "DOWN"

    def run(self) -> None:
        """ Game runner """
        print(" ---- STARTING GAME ----")
        while True:
            self.last_step = {
                "position": [self.x, self.y],
                "direction": self.direction
            }
            self.move()
            # Check if move is legal - if not game is terminated
            self._check_new_pos()
            # Print step info
            self.steps += 1
            self.print_step_info()


            # As a precautions step we limit the maximum number of steps taken
            if self.steps >= MAX_STEPS:
                self.complete_game()

    def move(self) -> None:
        """ Perform a single move """
        mover = {
            "UP": lambda: self._move_up(),
            "DOWN": lambda: self._move_down(),
            "LEFT": lambda: self._move_left(),
            "RIGHT": lambda: self._move_right(),
        }

        # Check if mirror in current room and if it changes course fo laser beam
        for mirror_room in self.board.mirror_rooms:
            if mirror_room.position == [self.x, self.y]:
                self.direction = mirror_room.get_output_dir(self.direction)

        # Perform a move in direction
        mover.get(self.direction)()

    def complete_game(self) -> None:
        dir = "V" if self.last_step["direction"] in ["UP", "DOWN"] else "H"
        print("--------- PUZZLE SOLVED ---------")
        print("-- Exit Room : {}".format(self.last_step["position"]))
        print("-- Exit Direction : {}".format(dir))

        ## NEED to find a way to gracefully exit game
        sys.exit()

    def _check_new_pos(self) -> None:
        """
        Check if new position is on or off board
        """
        # Check if position is on board if not on board - terminate game and produce game results
        if 0 <= self.x <= self.board.dim[0] and 0 <= self.y <= self.board.dim[1]:
            pass
        else:
            self.complete_game()

    def _move_left(self) -> None :
        self.x -= 1

    def _move_right(self) -> None:
        self.x += 1

    def _move_up(self) -> None:
        self.y += 1

    def _move_down(self) -> None:
        self.y -= 1

    def print_step_info(self) -> None:
        print("-- Step {} ::: Position {}, Direction {}".format(self.steps, [self.x, self.y], self.direction))

def main():
    # Input argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input",
        help="the input file containing game definition"
    )

    # Parse input arguments
    args = parser.parse_args()
    input_file = args.input
    game_specs = read_input(input_file)

    # Initialize and run game
    game = Game(game_specs["board_dimension"],
         game_specs["mirrors"],
         game_specs["laser_input"]
         )

    # Run Game
    game.run()

if __name__ == '__main__':
    main()