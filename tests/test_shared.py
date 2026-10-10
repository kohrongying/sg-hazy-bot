from unittest import TestCase
from shared import format_line, build_query_params


class SharedTest(TestCase):
    def test_format_line(self):
        self.assertEqual('| west    | 40    | 10    |',
                         format_line('west', 40, 10))

    
    def test_build_query_params_with_empty_response(self):
        self.assertEqual("", build_query_params([]))
