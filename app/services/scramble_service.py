import random
from app.constants import MODIFIERS, MOVES, OPPOSITE_FACES, WCA_SCRAMBLE_LENGTHS

class ScrambleService:
    @classmethod
    def generate_scramble(cls, puzzle: str = '3x3x3'):
        """
        Generate a scramble sequence for a given puzzle.

        Args:
            puzzle (str): The puzzle type (e.g., '2x2x2', '3x3x3', etc.). Defaults to '3x3x3'.

        Returns:
            List[str]: A list of moves representing the scramble sequence.

        Raises:
            ValueError: If the puzzle type is not supported.
        """

        if puzzle not in WCA_SCRAMBLE_LENGTHS:
            raise ValueError(f"Unsupported puzzle: {puzzle}")

        size = int(puzzle.split('x')[0])
        scramble_length = WCA_SCRAMBLE_LENGTHS[puzzle]

        if size in (2, 3):
            return cls._generate_2x3_scramble(scramble_length)
        elif size in (4, 5):
            return cls._generate_4x5_scramble(scramble_length)
        else:
            return cls._generate_large_cube_scramble(size, scramble_length)
        
    @classmethod
    def _generate_next_move(cls, prev_move: str):
        """
        Generate the next move while avoiding consecutive or opposite face moves.

        Args:
            prev_move (str): The previous move.

        Returns:
            str: The next move.
        """
        move = random.choice(MOVES)

        while OPPOSITE_FACES[move] == prev_move or prev_move == move:
            move = random.choice(MOVES)

        return move

    @classmethod
    def _generate_2x3_scramble(cls, scramble_length: int):
        """
        Generate a scramble for 2x2 or 3x3 puzzles.

        Args:
            scramble_length (int): The number of moves in the scramble.

        Returns:
            List[str]: A list of moves for the scramble.
        """
        scramble = []

        prev_move = random.choice(MOVES)
        scramble.append(prev_move + random.choice(MODIFIERS))

        for _ in range(scramble_length - 1):
            move = cls._generate_next_move(prev_move)
            prev_move = move

            move += random.choice(MODIFIERS)
            scramble.append(move)
            
        return scramble

    @classmethod
    def _generate_4x5_scramble(cls, scramble_length: int):
        """
        Generate a scramble for 4x4 or 5x5 puzzles.

        Args:
            scramble_length (int): The number of moves in the scramble.

        Returns:
            List[str]: A list of moves for the scramble.
        """
        wide_moves = ["", "w"]
        scramble = []

        prev_move = random.choice(MOVES)
        scramble.append(f'{prev_move}{random.choice(wide_moves)}{random.choice(MODIFIERS)}')

        for _ in range(scramble_length - 1):
            move = cls._generate_next_move(prev_move)
            prev_move = move

            move += f'{random.choice(wide_moves)}{random.choice(MODIFIERS)}'
            scramble.append(move)
        
        return scramble

    @classmethod
    def _generate_large_cube_scramble(cls, size: int, scramble_length: int):
        """
        Generate a scramble for larger cubes (e.g., 6x6 and above).

        Args:
            size (int): The size of the cube (e.g., 6 for 6x6x6).
            scramble_length (int): The number of moves in the scramble.

        Returns:
            List[str]: A list of moves for the scramble.
        """
        scramble = []
        half = size // 2    
        layers = ['']
        for i in range(2, half + 1):
            layers.append(str(i))

        prev_move = random.choice(MOVES)
        scramble.append(f'{random.choice(layers)}{prev_move}{random.choice(MODIFIERS)}')

        for _ in range(scramble_length - 1):
            prev_move = cls._generate_next_move(prev_move)

            move = f'{random.choice(layers)}{prev_move}{random.choice(MODIFIERS)}'
            scramble.append(move)
        
        return scramble
