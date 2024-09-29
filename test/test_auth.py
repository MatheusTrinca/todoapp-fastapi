import pytest
from fastapi import HTTPException
from starlette import status
from router.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from .utils import *
from jose import jwt
from datetime import timedelta

def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'test123', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user('wrong_username', 'test123', db)
    assert non_existent_user is False

    wrong_password = authenticate_user(test_user.username, 'wrong_password', db)
    assert wrong_password is False


def test_create_access_token(test_user):
    username = "matheustrinca"
    user_id = 1
    user_role = "admin"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, user_role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})

    assert decoded_token.get('sub') == username
    assert decoded_token.get('id') == user_id
    assert decoded_token.get('role') == user_role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'matheustrinca', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': 'matheustrinca', 'id': 1, 'role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate user"