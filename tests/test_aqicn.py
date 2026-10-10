from unittest import TestCase
from unittest.mock import patch
from aqicn import make_request, format_aqicn_response, get_aqicn_readings
from pathlib import Path
import json
import os

sample_response_filepath = Path.cwd() / "tests/sample_aqicn_response.json"
with open(sample_response_filepath) as f:
    mock_response = json.load(f)


class AqicnTest(TestCase):
    def test_format_aqicn_response(self):
        os.environ["DYNAMIC_MAP_BASE_URL"] = "https://example.com"
        with patch('aqicn.requests.get') as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = mock_response
            response = format_aqicn_response()
        self.assertEqual(
            """
<pre>
| Area    | PSI   | PM2.5 | 
|---------|-------|-------|
| north   | None  | 183   |
| south   | None  | 183   |
| east    | None  | 183   |
| west    | None  | 183   |
| central | None  | 183   |
</pre>
<a href="https://example.com?north=183&south=183&east=183&west=183&central=183">&#8205;</a>
    """, response)
