import pytest


def test_home_route_shows_start_page(client):
    with client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"Zapraszamy" in response.data


def test_lore_route_shows_lore_page(client):
    with client:
        response = client.get("/lore")
        assert response.status_code == 200
        assert b"Lore strony" in response.data
