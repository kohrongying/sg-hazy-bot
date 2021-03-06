from unittest import TestCase
from unittest.mock import patch
from api_service import make_request, get_psi_twenty_four_hourly, get_pm25_twenty_four_hourly, get_last_updated_time, \
    format_line, format_response, build_query_params
from pathlib import Path
import json
import os

sample_response_filepath = Path.cwd() / "tests/sample_response.json"
with open(sample_response_filepath) as f:
    mock_response = json.load(f)


class ApiServeTest(TestCase):
    def test_get_psi(self):
        with patch('api_service.requests.get') as mock_get:
            mock_get.return_value.ok = True
            response = make_request()
        self.assertIsNotNone(response)

    def test_get_psi_twenty_four_hourly(self):
        self.assertEqual({
            "west": 40,
            "national": 52,
            "east": 42,
            "central": 49,
            "south": 41,
            "north": 52
        }, get_psi_twenty_four_hourly(mock_response))

    def test_get_pm25_twenty_four_hourly(self):
        self.assertEqual({
            "west": 10,
            "national": 13,
            "east": 10,
            "central": 12,
            "south": 10,
            "north": 13
        }, get_pm25_twenty_four_hourly(mock_response))

    def test_get_last_updated_time(self):
        self.assertEqual('04 Apr 2021 16:08:53 SGT', get_last_updated_time(mock_response))

    def test_format_line(self):
        self.assertEqual('| west    | 40    | 10    |',
                         format_line('west', 40, 10))

    def test_format_response(self):
        psi = get_psi_twenty_four_hourly(mock_response)
        pm25 = get_pm25_twenty_four_hourly(mock_response)
        updated_time = get_last_updated_time(mock_response)
        os.environ["DYNAMIC_MAP_BASE_URL"] = "https://example.com"
        self.assertEqual(
            """
<pre>
| Area    | PSI   | PM2.5 | 
|---------|-------|-------|
| west    | 40    | 10    |
| east    | 42    | 10    |
| central | 49    | 12    |
| south   | 41    | 10    |
| north   | 52    | 13    |
</pre>
<em>Last updated on 04 Apr 2021 16:08:53 SGT</em>
<a href="https://example.com?west=40&east=42&central=49&south=41&north=52">&#8205;</a>
    """, format_response(psi, pm25, updated_time))

    def test_build_query_params(self):
        psi = get_psi_twenty_four_hourly(mock_response)
        self.assertEqual("?west=40&east=42&central=49&south=41&north=52", build_query_params(psi))

    def test_build_query_params_with_empty_response(self):
        self.assertEqual("", build_query_params({}))
