from fastapi.testclient import TestClient
from main import app, save_todos


client = TestClient(app)


def setup_function():
    # reset storage before each test
    save_todos([])


def test_get_todos_initially_empty():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {"todos": []}


def test_add_todo_and_toggle_and_delete():
    # add
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 200
    todo = response.json()
    assert todo["title"] == "Buy milk"
    assert todo["done"] is False

    # toggle
    response = client.patch(f"/todos/{todo['id']}")
    assert response.status_code == 200
    toggled = response.json()
    assert toggled["done"] is True

    # delete
    response = client.delete(f"/todos/{todo['id']}")
    assert response.status_code == 200
    assert response.json() == {"deleted": todo["id"]}

