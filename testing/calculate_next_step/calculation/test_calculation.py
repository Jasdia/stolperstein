# Python-libraries
from unittest import TestCase
from os import walk
from json import loads
from pathlib import Path
from multiprocessing import Process, Value

# Other modules from this project
# global variables (see conventions in *_global_variables.py):
import api.api_feedback_global_variables as api_globals
import calculate_next_step.mc_global_variables as mc_globals
# functions:
from calculate_next_step.calculation import _calculate_move, _test_all_options, _move_iteration
# dataclasses:
from data_classes.manual_calculation.ManuelCalculatedGame import ManuelCalculatedGame
from data_classes.manual_calculation.ManuelCalculatedPlayer import ManuelCalculatedPlayer


def load_an_ManuelCalculatedGame_object(path: str, i: str):
    tmp_file = open(path + "/" + i + "_data.json", "r")
    test_data = loads(tmp_file.read())
    tmp_file.close()
    test_data["players"] = [ManuelCalculatedPlayer(**player) for player in test_data["players"].values()]
    return ManuelCalculatedGame(**test_data)


def load_files(path: str, i: str):
    test_data_class = load_an_ManuelCalculatedGame_object(path, i)

    tmp_file = open(path + "/" + i + "_parameters.json", "r")
    parameters = loads(tmp_file.read())
    tmp_file.close()

    tmp_file = open(path + "/" + str(i) + "_result.json", "r")
    result_data = loads(tmp_file.read())
    tmp_file.close()

    return test_data_class, parameters, result_data


class TestCalculation(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCalculation, self).__init__(*args, **kwargs)
        self._root_path = str(Path(__file__).parent.absolute())
        api_globals._init()
        mc_globals._init()

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

            result_data = (result_data["death_count"], result_data["killed_count"])
            test_result = (Value("i", 0), Value("i", 0))

            _test_all_options(parameters["position"], test_result[0], test_result[1], test_data_class,
                              parameters["test_depth"], parameters["is_not_6th_step"], mc_globals.move_list)
            with test_result[0].get_lock() and test_result[1].get_lock():
                self.assertEqual(result_data, (test_result[0].value, test_result[1].value),
                                 msg="_test_all_options number: " + str(i) + " failed.")

    def test__move_iteration(self):
        path = self._root_path + "/_move_iteration"
        files = next(walk(path))[2]
        count = len(files)
        for i in range(int(count / 3)):
            test_data_class, parameters, result_data = load_files(path, str(i))

            api_globals.amount_of_moves = parameters["api_globals.amount_of_moves"]

            result_data = (result_data["api_globals.action"], result_data["mc_globals.highest_test_step"])

            _move_iteration(parameters["test_depth"], parameters["step"], test_data_class)
            test_result = (api_globals.action, mc_globals.highest_test_step)
            self.assertEqual(result_data, test_result, msg="_test_all_options number: " + str(i) + " failed.")
