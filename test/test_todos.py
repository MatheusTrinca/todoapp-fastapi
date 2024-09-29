from starlette import status
from router.todos import get_db, get_current_user

from test.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title': "Todo test title",
                                'description': "Todo test description",
                                'priority': 5,
                                'complete': False,
                                'id': 1,
                                'owner_id': 1}]


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'title': "Todo test title",
                                'description': "Todo test description",
                                'priority': 5,
                                'complete': False,
                                'id': 1,
                                'owner_id': 1}


def test_read_one_authenticated_not_found():
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(test_todo):
    request_data = {
        "title": "Test new todo",
        "description": "Test new todo description",
        "priority": 5,
        "complete": False
    }

    response = client.post("/todos", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 2).first()
    assert todo.title == request_data.get("title")
    assert todo.description == request_data.get("description")
    assert todo.priority == request_data.get("priority")
    assert todo.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        "title": "Test new todo changed title",
        "description": "Test new todo description",
        "priority": 5,
        "complete": False
    }

    response = client.put("/todos/1", json=request_data)
    assert response.status_code == status.HTTP_200_OK

    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo.title == request_data.get("title")


def test_update_todo_not_found():
    request_data = {
        "title": "Test new todo changed title",
        "description": "Test new todo description",
        "priority": 5,
        "complete": False
    }

    response = client.put("/todos/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with id 999 not found"}


def test_delete_todo(test_todo):
    response = client.delete("/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo is None


def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with id 999 not found"}