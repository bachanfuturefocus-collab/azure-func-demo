import sys
from pathlib import Path
import json
import azure.functions as func

# Add project root to sys.path so Python can find HttpTrigger
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from HttpTrigger import main  # ✅ correct import

class DummyReq:
    def __init__(self, json_data=None, params=None):
        self._json = json_data
        self._params = params or {}

    def get_json(self):
        if self._json is None:
            raise ValueError("No JSON")
        return self._json

    @property
    def params(self):
        return self._params

def test_post_with_json():
    req = DummyReq(json_data={"name": "Bachan"})
    resp = main(req)
    assert resp.status_code == 200
    body = json.loads(resp.get_body())
    assert body["message"] == "Hello, Bachan!"

def test_get_with_query():
    req = DummyReq(json_data=None, params={"name": "Bro"})
    resp = main(req)
    assert resp.status_code == 200
    body = json.loads(resp.get_body())
    assert body["message"] == "Hello, Bro!"

def test_missing_name_returns_400():
    req = DummyReq(json_data=None, params={})
    resp = main(req)
    assert resp.status_code == 400
    body = json.loads(resp.get_body())
    assert "error" in body
