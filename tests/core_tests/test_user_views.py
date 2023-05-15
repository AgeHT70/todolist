import json

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_user(client, get_user_data):
    url = reverse('core:signup')
    data = get_user_data

    response = client.post(
        url,
        data,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {
        'username': 'test_username',
        'email': 'testemail@test.com',
        'first_name': '',
        'last_name': '',
    }


@pytest.mark.django_db
def test_login(client, get_user_data, django_user_model) -> None:
    url = reverse('core:login')
    get_user_data.pop('password_repeat')
    user = django_user_model.objects.create_user(**get_user_data)

    response = client.post(url, data=get_user_data, content_type='application/json')
    result = response.json()

    assert response.status_code == 200
    assert result['username'] == user.username


@pytest.mark.django_db
def test_update(client, get_user_data, auth_user) -> None:
    url = reverse('core:profile')
    get_user_data.pop('password_repeat')
    get_user_data['email'] = 'new_email@test.com'

    response = auth_user.put(url, data=get_user_data, content_type='application/json')
    result = response.json()

    assert response.status_code == 200
    assert result['email'] == get_user_data['email']
