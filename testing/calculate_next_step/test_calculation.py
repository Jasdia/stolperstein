# Python-libraries
from unittest import TestCase
from os import walk
from pathlib import Path
from multiprocessing import Value
from ctypes import c_int

# Other modules from this project
# global variables:
import global_variables as internal_globals
# functions:
from calculate_next_step.calculation import move_iteration, _calculate_move, _test_all_options
from testing.calculate_next_step.loadingfunctions_for_the_test import load_files
# dataclasses:
from data_classes.ManuelCalculatedGame import ManuelCalculatedGame
from data_classes.ManuelCalculatedPlayer import ManuelCalculatedPlayer


class TestCalculation(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCalculation, self).__init__(*args, **kwargs)
        self._root_path = str(Path(__file__).parent.absolute())
        internal_globals._init()

    def test__calculate_move(self):
        path = self._root_path + "/_calculate_move"
        files = next(walk(path))[2]
        count = len(files)
        for i in range(int(count / 3)):
            test_data_class, parameters, result_data = load_files(path, str(i))

            result_data["players"] = [ManuelCalculatedPlayer(**player) for player in result_data["players"].values()]
            result_data_class = ManuelCalculatedGame(**result_data)

            test_result = _calculate_move(parameters["position"], parameters["action"], test_data_class,
                                          parameters["is_not_6th_step"])
            self.assertEqual(result_data_class, test_result, msg="_calculate_move number: " + str(i) + " failed.")

    def test__test_all_options(self):
        path = self._root_path + "/_test_all_options"
        files = next(walk(path))[2]
        count = len(files)
        for i in range(int(count / 3)):
            test_data_class, parameters, result_data = load_files(path, str(i))

            result_data = (result_data["death_count"], result_data["kill_count"])
            test_result = (Value("i", 0), Value("i", 0))

            _test_all_options(parameters["position"], test_result[0], test_result[1], test_data_class,
                              parameters["is_not_6th_step"], internal_globals.move_list)
            with test_result[0].get_lock() and test_result[1].get_lock():
                self.assertEqual(result_data, (test_result[0].value, test_result[1].value),
                                 msg="_test_all_options number: " + str(i) + " failed.")

    def test_move_iteration(self):
        path = self._root_path + "/move_iteration"
        files = next(walk(path))[2]
        count = len(files)
        for i in range(int(count / 3)):
            test_data_class, parameters, result_data = load_files(path, str(i), False)

            action = Value(c_int, parameters["action"])
            amount_of_moves = Value("i", parameters["amount_of_moves"])

            move_iteration(parameters["step"], test_data_class, action, amount_of_moves, internal_globals.move_list)
            with action.get_lock():
                self.assertEqual(result_data["action"], internal_globals.move_list[action.value],
                                 msg="_test_all_options number: " + str(i) + " failed.")
