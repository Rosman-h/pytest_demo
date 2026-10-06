"""
Name: Rami Osman
SID: 004003896

This program finds dictionary words on a Boggle board.
"""

MIN_WORD_LENGTH = 3

# The eight neighbors of a tile: (row change, column change).
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
]


class Boggle:
    """Stores a Boggle grid and dictionary and finds the words in it."""

    def __init__(self, grid, dictionary):
        """Sets up the grid, dictionary, and solution list."""
        self.grid = grid
        self.dictionary = dictionary
        self.solution = []

    def setGrid(self, grid):
        """Replaces the grid and clears any old solution."""
        self.grid = grid
        self.solution = []

    def setDictionary(self, dictionary):
        """Replaces the dictionary and clears any old solution."""
        self.dictionary = dictionary
        self.solution = []

    def _is_valid_input(self):
        """Returns True if the grid is a square list of non-empty
        strings and the dictionary is a list of strings."""
        if not isinstance(self.grid, list) or len(self.grid) == 0:
            return False
        if not isinstance(self.dictionary, list):
            return False

        size = len(self.grid)
        for row in self.grid:
            if not isinstance(row, list) or len(row) != size:
                return False
            for tile in row:
                if not isinstance(tile, str) or tile == "":
                    return False

        for word in self.dictionary:
            if not isinstance(word, str):
                return False
        return True

    def _build_prefixes(self, words):
        """Returns every prefix of every word, so dead paths stop early."""
        prefixes = set()
        for word in words:
            for end in range(1, len(word) + 1):
                prefixes.add(word[:end])
        return prefixes

    def _search(self, row, column, current, used, words, prefixes, found):
        """Extends the path through (row, column) using depth-first search.

        current is the text spelled so far, used holds the tiles on the
        path, and found collects every dictionary word reached.
        """
        size = len(self.grid)
        if row < 0 or row >= size or column < 0 or column >= size:
            return
        if (row, column) in used:
            return

        current = current + self.grid[row][column].lower()
        if current not in prefixes:
            return

        if current in words:
            found.add(current)

        used.add((row, column))
        for row_move, column_move in DIRECTIONS:
            self._search(row + row_move, column + column_move,
                         current, used, words, prefixes, found)
        used.remove((row, column))

    def getSolution(self):
        """Returns the dictionary words found on the grid.

        Returns an empty list if nothing is found or the input is invalid.
        """
        self.solution = []
        if not self._is_valid_input():
            return []

        words = set()
        for word in self.dictionary:
            if len(word) >= MIN_WORD_LENGTH:
                words.add(word.lower())
        prefixes = self._build_prefixes(words)

        found = set()
        for row in range(len(self.grid)):
            for column in range(len(self.grid)):
                self._search(row, column, "", set(), words, prefixes, found)

        # Keep the caller's spelling and the dictionary's order.
        for word in self.dictionary:
            lowered = word.lower()
            if lowered in found and word not in self.solution:
                self.solution.append(word)
        return self.solution


def main():
    """Runs the Boggle solver on a sample grid."""
    grid = [["A", "B", "C", "D"],
            ["E", "F", "G", "H"],
            ["Ie", "J", "K", "L"],
            ["A", "B", "C", "D"]]
    dictionary = ["ABEF", "AFJIEB", "DGKD", "DGKA"]

    mygame = Boggle(grid, dictionary)
    print(mygame.getSolution())


if __name__ == "__main__":
    main()
