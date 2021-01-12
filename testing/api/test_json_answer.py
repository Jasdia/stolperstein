# Python-libraries
from unittest import TestCase
from json import loads

# Other modules from this project
# functions:
from api.json_answer import generated_json


class TestJsonAnswer(TestCase):

    def test_json_answer(self):

        self.assertEqual('{"action": "change_nothing"}', generated_json(f'{"change_nothing"}'))
