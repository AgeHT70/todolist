import pytest


def test_get_category_list_not_auth_user(client):
    response = client.get('/goals/goal_category/list')

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_category_not_auth_user(client, board_create):
    board = board_create
    category_data = {
        'title': 'Test_Category',
        'board': board.id,
    }

    response = client.post(
        '/goals/goal_category/create',
        data=category_data,
        content_type='application/json',
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_category_auth_user(get_board_with_owner):
    board, client = get_board_with_owner
    category_data = {
        'title': 'Test_Category',
        'board': board.id,
    }

    response = client.post(
        '/goals/goal_category/create',
        data=category_data,
        content_type='application/json',
    )

    assert response.status_code == 201
    assert response.data['title'] == category_data['title']


@pytest.mark.django_db
def test_update_category_auth_user(create_category):
    category, client = create_category

    response = client.patch(
        f'/goals/goal_category/{category.id}',
        {'title': 'updated_title'},
        content_type='application/json',
    )

    assert response.status_code == 200
    assert response.data['title'] == 'updated_title'


@pytest.mark.django_db
def test_delete_category_auth_user(create_category):
    category, client = create_category

    response = client.delete(
        f'/goals/goal_category/{category.id}',
        {'title': 'updated_title'},
        content_type='application/json',
    )

    assert response.status_code == 204
