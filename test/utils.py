from sqlalchemy import text, create_engine
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base
import pytest
from models import Todos, Users
from main import app
from router.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'matheustrinca', 'id': 1, 'role': 'admin'}

client = TestClient(app)

@pytest.fixture()
def test_todo():
    todo = Todos(
        title="Todo test title",
        description="Todo test description",
        priority=5,
        complete=False,
        owner_id= 1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()


@pytest.fixture()
def test_user():
    user = Users(
        username = "matheustrinca",
        email = "matheustrinca@gmail.com",
        first_name = "Matheus",
        last_name = "Trinca",
        hashed_password = bcrypt_context.hash("test123"),
        role = "admin",
        phone_number = "123456"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()