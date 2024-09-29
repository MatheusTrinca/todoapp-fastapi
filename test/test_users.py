from starlette import status
from router.users import get_db, get_current_user
from .utils import *
from models import Users

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('username') == "matheustrinca"


def test_change_password_success(test_user):
    request_data = {
        "password": "test123",
        "new_password": "test123456"
    }

    response = client.put("/user/password", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    request_data = {
        "password": "test1234",
        "new_password": "test123456"
    }

    response = client.put("/user/password", json=request_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Failed authentication"}


def test_update_phone_number(test_user):
    request_data = {"phone_number": "987654321"}
    response = client.put("/user", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    user = db.query(Users).filter(Users.id == 1).first()

    assert user.phone_number == request_data.get('phone_number')
