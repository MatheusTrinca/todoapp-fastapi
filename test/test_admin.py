from starlette import status
from router.admin import get_db, get_current_user
from .utils import *
from models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_user(test_todo):
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Todo test title",
        "description": "Todo test description",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }]


def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo is None


def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with id 999 not found"}
