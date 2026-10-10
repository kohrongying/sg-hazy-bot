from unittest import TestCase
from unittest.mock import patch
from nea import make_request, format_nea_response, get_last_updated_time
from pathlib import Path
import json
import os

sample_response_filepath = Path.cwd() / "tests/sample_response.json"
with open(sample_response_filepath) as f:
    mock_response = json.load(f)


class NeaTest(TestCase):
    def test_get_psi(self):
        with patch('nea.requests.get') as mock_get:
            mock_get.return_value.ok = True
            response = make_request()
        self.assertIsNotNone(response)

    def test_get_last_updated_time(self):
        self.assertEqual('04 Apr 2021 16:08:53 SGT', get_last_updated_time(mock_response))

    def test_format_nea_response(self):
        os.environ["DYNAMIC_MAP_BASE_URL"] = "https://example.com"
        with patch('nea.requests.get') as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = mock_response
            response = format_nea_response()
        self.assertEqual(
            """
<pre>
| Area    | PSI   | PM2.5 | 
|---------|-------|-------|
| north   | 52    | 13    |
| south   | 41    | 10    |
| east    | 42    | 10    |
| west    | 40    | 10    |
| central | 49    | 12    |
</pre>
<em>Last updated on 04 Apr 2021 16:08:53 SGT</em>
<a href="https://example.com?north=52&south=41&east=42&west=40&central=49">&#8205;</a>
    """, response)
