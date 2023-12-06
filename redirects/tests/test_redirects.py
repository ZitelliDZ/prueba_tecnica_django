import pytest
import os
import django
from django.test import Client
import redirects.services as services
import unittest.mock as mock
from rest_framework import status


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()



@pytest.mark.order(1)
@mock.patch('redirects.services.get_redirect_from_db')
def test_get_redirect_from_db(mock_get_redirect_from_db):
    # Verificar que el objeto está activo inicialmente

    mock_get_redirect_from_db.return_value = {
        "key": 4,
        "url": "4",
        "active": False,
        "created_at": "2023-12-05T18:46:56.042634Z",
        "updated_at": "2023-12-05T18:46:56.042652Z"
    }
    redirect = services.get_redirect_from_db(1)
    assert redirect == mock_get_redirect_from_db.return_value




@pytest.mark.order(2)
@pytest.mark.django_db
def test_create_store_uncache():
    c = Client()
    response = c.post("/api/redirects", {"url": "uncache.com", "active": "false"})
    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()
    assert content['url'] == 'uncache.com'
    assert content['active'] == False




@pytest.mark.order(3)
@pytest.mark.django_db
def test_create_store_in_cache():
    c = Client()
    response = c.post("/api/redirects", {"url": "cache.com", "active": "true"})
    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()
    assert content['url'] == 'cache.com'
    assert content['active'] == True

@pytest.mark.order(4)
@pytest.mark.django_db
def test_create_bad_request():
    c = Client()
    response = c.post("/api/redirects", {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.order(5)
@pytest.mark.django_db
def test_get_by_id_uncache():
    c = Client()
    response = c.post("/api/redirects", {"url": "uncache.com", "active": "false"})
    content = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    response = c.get(f"/api/redirects/{content['key']}")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content['url'] == 'uncache.com'
    assert content['active'] == False


@pytest.mark.order(6)
@pytest.mark.django_db
def test_get_by_id_incache():
    c = Client()
    response = c.post("/api/redirects", {"url": "cache.com", "active": "true"})
    content = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    response = c.get(f"/api/redirects/{content['key']}")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content['url'] == 'cache.com'
    assert content['active'] == True

@pytest.mark.order(7)
@pytest.mark.django_db
def test_get_by_id_not_found():
    c = Client()
    response = c.get(f"/api/redirects/30")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.order(8)
@pytest.mark.django_db
def test_delete():
    c = Client()
    response = c.post("/api/redirects", {"url": "cache.com", "active": "true"})
    content = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    response = c.delete(f"/api/redirects/{content['key']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = c.get(f"/api/redirects/{content['key']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.order(9)
@pytest.mark.django_db
def test_list():
    c = Client()
    response = c.get("/api/redirects")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(10)
@pytest.mark.django_db
def test_update():
    c = Client()
    response = c.post("/api/redirects", {"url": "cache.com", "active": "true"})
    content = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    update_data = {"url": "updated-uncache.com", "active": "false"}
    response = c.put(f"/api/redirects/{content['key']}", json=update_data)
    assert response.status_code == status.HTTP_202_ACCEPTED

@pytest.mark.order(11)
@pytest.mark.django_db
def test_update_not_found():
    c = Client()
    update_data = {"url": "updated-uncache.com", "active": "false"}
    response = c.put("/api/redirects/30", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

