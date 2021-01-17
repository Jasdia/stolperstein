# Python-libraries
from unittest import TestCase
from os import walk
from pathlib import Path

# Other modules from this project
# functions:
from testing.loadingfunctions_for_the_test import load_files
from calculate_next_step.data_simplification import simplify_game_data, _simple_player_mapping
# dataclasses:
from data_classes.ManuelCalculatedGame import ManuelCalculatedGame
from data_classes.ManuelCalculatedPlayer import ManuelCalculatedPlayer


class TestDateSimplification(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDateSimplification, self).__init__(*args, **kwargs)
        self._root_path = str(Path(__file__).parent.absolute())

    def test_simplify_game_data(self):
        path = self._root_path + "/simplify_game_data"
        files = next(walk(path))[2]
        count = len(files)
        for i in range(int(count / 2)):
            test_data_class, result_data = load_files(path, str(i), False, False)

            result_data["players"] = [ManuelCalculatedPlayer(**player) for player in result_data["players"]]
            result_data_class = ManuelCalculatedGame(**result_data)

            test_result = simplify_game_data(test_data_class)
            self.assertEqual(result_data_class, test_result)

    def test__simple_player_mapping(self):
        path = self._root_path + "/_simple_player_mapping"
        files = next(walk(path))[2]
        count = len(files)
        for i in range(int(count / 2)):
            test_data, parameter, result_data = load_files(path, str(i), False)

            result_data_class = ManuelCalculatedPlayer(**result_data)

            test_result = _simple_player_mapping(test_data, parameter["ID"])

            self.assertEqual(result_data_class, test_result)
