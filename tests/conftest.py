import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import hash_password
from app.database import Base, get_db
from app.main import app
from app.models import User


@pytest.fixture()
def db_session():
    # Levantamos db de testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture()
def demo_user(db_session):
        # Seed de usuario demo
        demo_user = User(
            username="demouser",
            password_hash=hash_password("demopassword")
        )
        db_session.add(demo_user)
        db_session.commit()
        db_session.refresh(demo_user)
        return demo_user

@pytest.fixture()
# Parametro 'no usado' es necesario para que pytest ejecute este fixture antes de los tests
def authenticated_client(client, demo_user):
    response = client.post(
            "/login", 
            data={
               "username": "demouser", 
               "password": "demopassword"
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    return client

