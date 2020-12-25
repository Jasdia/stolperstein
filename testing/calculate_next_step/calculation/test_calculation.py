import unittest
import os
from json import loads
from pathlib import Path

from calculate_next_step.calculation import _set_move
from data_classes.manual_calculation.ManuelCalculatedGame import ManuelCalculatedGame
from data_classes.manual_calculation.ManuelCalculatedPlayer import ManuelCalculatedPlayer
import api.api_feedback_global_variables as api_globals


class TestCalculation(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCalculation, self).__init__(*args, **kwargs)
        self._root_path = str(Path(__file__).parent.absolute())
        self.path = self._root_path + "/res"
        api_globals._init()

    def test__set_move(self):
        files = next(os.walk(self.path))[2]
        count = len(files)
        print()
        for i in range(int(count/3)):
            tmp_file = open(self.path + "/" + str(i) + "_data.json", "r")
            test_data = loads(tmp_file.read())
            tmp_file.close()
            test_data["players"] = [ManuelCalculatedPlayer(**player) for player in test_data["players"].values()]
            test_data_class = ManuelCalculatedGame(**test_data)

            tmp_file = open(self.path + "/" + str(i) + "_parameters.json", "r")
            parameters = loads(tmp_file.read())
            tmp_file.close()

            api_globals.amount_of_moves = parameters["api_globals.amount_of_moves"]

            tmp_file = open(self.path + "/" + str(i) + "_result.json", "r")
            result_data = loads(tmp_file.read())
            tmp_file.close()
            result_data["players"] = [ManuelCalculatedPlayer(**player) for player in result_data["players"].values()]
            result_data_class = ManuelCalculatedGame(**result_data)

            test_result = _set_move(parameters["position"], parameters["action"], test_data_class)
            self.assertEqual(result_data_class, test_result, msg="_set_move-test number: " + str(i) + " failed.")
