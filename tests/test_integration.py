# tests/test_integration.py
import requests

BASE_URL = "http://3.34.155.126:8002"

def test_root():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200

def test_todos():
    r = requests.get(f"{BASE_URL}/todos")
    assert r.status_code in [200, 404]  # 엔드포인트에 따라 다름
