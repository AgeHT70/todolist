import pytest
from django.urls import reverse

from goals.models import Board, BoardParticipant


@pytest.mark.django_db
def test_create_board(client, auth_user):
    url = reverse('goals:board-create')
    data = {'title': 'test_board'}

    response = auth_user.post(url, data, content_type='application/json')
    assert response.status_code == 201
    assert response.data['title'] == data['title']


def test_get_board(get_board_with_owner):
    board, client = get_board_with_owner
    response = client.get(f'/goals/board/{board.id}')
    assert response.status_code == 200
    assert response.data['title'] == board.title


@pytest.mark.django_db
def test_get_board_not_auth_user(client, django_user_model, board_create):
    board = board_create
    user_data = {'username': 'test_username', 'password': 'test_password'}
    user = django_user_model.objects.create_user(**user_data)
    BoardParticipant.objects.create(board=board, role=BoardParticipant.Role.owner, user=user)
    response = client.get(f'/goals/board/{board.id}')
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_board(get_board_with_owner):
    board, client = get_board_with_owner
    new_board = {'title': 'new_test_board'}
    response = client.patch(f'/goals/board/{board.id}', new_board, content_type='application/json')
    assert response.status_code == 200
    assert response.data['title'] == new_board['title']


@pytest.mark.django_db
def test_update_board_not_owner(board_create, client, django_user_model):
    board = board_create
    new_board = {'title': 'new_test_board'}
    user_data = {'username': 'test_username', 'password': 'test_password'}
    user = django_user_model.objects.create_user(**user_data)
    BoardParticipant.objects.create(board=board, role=BoardParticipant.Role.reader, user=user)
    client.force_login(user)
    response = client.patch(f'/goals/board/{board.id}', new_board, content_type='application/json')
    assert response.status_code == 403


def test_delete_board(get_board_with_owner):
    board, client = get_board_with_owner
    response = client.delete(f'/goals/board/{board.id}')
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_board_not_owner(board_create, client, django_user_model):
    board = board_create
    new_board = {'title': 'new_test_board'}
    user_data = {'username': 'test_username', 'password': 'test_password'}
    user = django_user_model.objects.create_user(**user_data)
    BoardParticipant.objects.create(board=board, role=BoardParticipant.Role.reader, user=user)
    client.force_login(user)
    response = client.delete(f'/goals/board/{board.id}', new_board, content_type='application/json')
    assert response.status_code == 403
