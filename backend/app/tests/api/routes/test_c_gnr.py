from fastapi.testclient import TestClient

from app.core.config import settings


def test_c_gnr_without_model_returns_503(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/c_gnr/",
        headers=superuser_token_headers,
        json={"input": "def add(a, b):"},
    )
    assert r.status_code == 503
