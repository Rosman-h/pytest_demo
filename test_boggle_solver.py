"""
Name: Rami Osman
SID: 004003896

Black-box unit tests for the Boggle solver.

Each test maps to one test frame from the Category Partition Method.
Tests only call the public API (Boggle, setGrid, setDictionary,
getSolution) and never look at the solver's internals.
"""

import unittest

from boggle_solver import Boggle

# The board from the assignment, with "St" and "Qu" tiles.
ST_QU_GRID = [["T", "W", "Y", "R"],
              ["E", "N", "P", "H"],
              ["G", "St", "Qu", "R"],
              ["O", "N", "T", "A"]]

# A 4x4 board with a multi-letter "Ie" tile.
IE_GRID = [["A", "B", "C", "D"],
           ["E", "F", "G", "H"],
           ["Ie", "J", "K", "L"],
           ["A", "B", "C", "D"]]

TWO_BY_TWO = [["A", "B"],
              ["C", "D"]]

THREE_BY_THREE = [["A", "B", "C"],
                  ["D", "E", "F"],
                  ["G", "H", "J"]]

FIVE_BY_FIVE = [["A", "B", "C", "D", "E"],
                ["F", "G", "H", "I", "J"],
                ["K", "L", "M", "N", "O"],
                ["P", "Q", "R", "S", "T"],
                ["U", "V", "W", "X", "Y"]]


class TestBoggleInvalidInput(unittest.TestCase):
    """Frames where the grid or dictionary is invalid: expect []."""

    def test_empty_dictionary(self):
        self.assertEqual(Boggle(TWO_BY_TWO, []).getSolution(), [])

    def test_empty_grid(self):
        self.assertEqual(Boggle([], ["abc"]).getSolution(), [])

    def test_grid_is_none(self):
        self.assertEqual(Boggle(None, ["abc"]).getSolution(), [])

    def test_dictionary_is_none(self):
        self.assertEqual(Boggle(TWO_BY_TWO, None).getSolution(), [])

    def test_non_square_grid(self):
        grid = [["A", "B", "C"], ["D", "E", "F"]]
        self.assertEqual(Boggle(grid, ["abc"]).getSolution(), [])

    def test_grid_with_non_string_tile(self):
        grid = [["A", 1], ["C", "D"]]
        self.assertEqual(Boggle(grid, ["acd"]).getSolution(), [])


class TestBoggleGridSizes(unittest.TestCase):
    """Frames covering different grid sizes."""

    def test_one_by_one_grid(self):
        self.assertEqual(Boggle([["A"]], ["a", "aa", "aaa"]).getSolution(),
                         [])

    def test_two_by_two_spec_example(self):
        dictionary = ["A", "B", "AC", "ACA", "ACB", "DE"]
        self.assertCountEqual(Boggle(TWO_BY_TWO, dictionary).getSolution(),
                              ["ACB"])

    def test_three_by_three_grid(self):
        self.assertCountEqual(
            Boggle(THREE_BY_THREE, ["ABE", "ACE"]).getSolution(), ["ABE"])

    def test_five_by_five_diagonal_words(self):
        dictionary = ["AGM", "AGMSY"]
        self.assertCountEqual(
            Boggle(FIVE_BY_FIVE, dictionary).getSolution(), dictionary)


class TestBoggleAdjacencyRules(unittest.TestCase):
    """Frames covering how tiles may be connected."""

    def test_diagonal_move_is_allowed(self):
        self.assertCountEqual(Boggle(TWO_BY_TWO, ["ADB"]).getSolution(),
                              ["ADB"])

    def test_non_adjacent_tiles_are_rejected(self):
        # A and C are two columns apart in the top row.
        self.assertEqual(Boggle(THREE_BY_THREE, ["ACE"]).getSolution(), [])

    def test_tile_cannot_be_reused_in_one_word(self):
        # The grid has only one A, so ABA is impossible.
        self.assertEqual(Boggle(TWO_BY_TWO, ["ABA"]).getSolution(), [])

    def test_all_tiles_can_be_used_once(self):
        grid = [["A", "A"], ["A", "A"]]
        dictionary = ["AAA", "AAAA", "AAAAA"]
        self.assertCountEqual(Boggle(grid, dictionary).getSolution(),
                              ["AAA", "AAAA"])


class TestBoggleWordRules(unittest.TestCase):
    """Frames covering word length, case, and duplicates."""

    def test_words_shorter_than_three_letters_are_ignored(self):
        self.assertCountEqual(
            Boggle(TWO_BY_TWO, ["AB", "ABC"]).getSolution(), ["ABC"])

    def test_word_not_on_board(self):
        self.assertEqual(Boggle(TWO_BY_TWO, ["XYZ"]).getSolution(), [])

    def test_dictionary_case_is_kept(self):
        self.assertCountEqual(
            Boggle(ST_QU_GRID, ["ART", "Art"]).getSolution(),
            ["ART", "Art"])

    def test_duplicate_dictionary_words_returned_once(self):
        self.assertCountEqual(
            Boggle(ST_QU_GRID, ["art", "art"]).getSolution(), ["art"])


class TestBoggleMultiLetterTiles(unittest.TestCase):
    """Frames covering the Qu, St, and Ie tiles."""

    def test_qu_tile_words(self):
        dictionary = ["qua", "quart", "quartz"]
        self.assertCountEqual(
            Boggle(ST_QU_GRID, dictionary).getSolution(),
            ["qua", "quart"])

    def test_st_tile_words(self):
        dictionary = ["stont", "stqura"]
        self.assertCountEqual(
            Boggle(ST_QU_GRID, dictionary).getSolution(), dictionary)

    def test_ie_tile_words(self):
        dictionary = ["ABEF", "AFJIEB", "DGKD", "DGKA"]
        self.assertCountEqual(
            Boggle(IE_GRID, dictionary).getSolution(),
            ["ABEF", "AFJIEB", "DGKD"])

    def test_q_without_u_is_not_a_tile(self):
        self.assertEqual(Boggle(ST_QU_GRID, ["qat"]).getSolution(), [])

    def test_s_without_t_is_not_a_tile(self):
        self.assertEqual(Boggle(ST_QU_GRID, ["sat"]).getSolution(), [])


class TestBoggleSpecBoard(unittest.TestCase):
    """The full valid and invalid word lists from the assignment."""

    def test_valid_and_invalid_words(self):
        valid = ["art", "ego", "gent", "get", "net", "new", "newt",
                 "prat", "pry", "qua", "quart", "rat", "tar", "tarp",
                 "ten", "went", "wet"]
        invalid = ["arty", "egg", "not"]
        self.assertCountEqual(
            Boggle(ST_QU_GRID, valid + invalid).getSolution(), valid)


class TestBoggleSetters(unittest.TestCase):
    """Frame covering setGrid and setDictionary."""

    def test_set_grid_and_dictionary(self):
        game = Boggle([], [])
        game.setGrid(TWO_BY_TWO)
        game.setDictionary(["ACB"])
        self.assertCountEqual(game.getSolution(), ["ACB"])


if __name__ == "__main__":
    unittest.main()
