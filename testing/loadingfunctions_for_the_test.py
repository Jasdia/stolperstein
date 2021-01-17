# Python-libraries
from json import loads

# Other modules from this project
# dataclasses:
from data_classes.ManuelCalculatedGame import ManuelCalculatedGame
from data_classes.ManuelCalculatedPlayer import ManuelCalculatedPlayer


def _load_an_ManuelCalculatedGame_object(path: str, i: str, interpret_dataclass: bool):
    tmp_file = open(path + "/" + i + "_data.json", "r")
    test_data = loads(tmp_file.read())
    tmp_file.close()
    if interpret_dataclass:
        test_data["players"] = [ManuelCalculatedPlayer(**player) for player in test_data["players"].values()]
        return ManuelCalculatedGame(**test_data)
    else:
        return test_data


def load_files(path: str, i: str, interpret_dataclass: bool = True, needs_parameters: bool = True):
    test_data_class = _load_an_ManuelCalculatedGame_object(path, i, interpret_dataclass)

    tmp_file = open(path + "/" + str(i) + "_result.json", "r")
    result_data = loads(tmp_file.read())
    tmp_file.close()

    if needs_parameters:
        tmp_file = open(path + "/" + i + "_parameters.json", "r")
        parameters = loads(tmp_file.read())
        tmp_file.close()

        return test_data_class, parameters, result_data

    return test_data_class, result_data
