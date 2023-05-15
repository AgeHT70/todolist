import pytest


@pytest.mark.django_db
def test_create_goal_auth_user(create_category):
    category, client = create_category
    goal_data = {'title': 'Test_Goal', 'category': category.id}
    response = client.post('/goals/goal/create', data=goal_data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_goal_auth_user(create_goal):
    goal, client = create_goal
    update_data = {'title': 'new_test_goal'}
    response = client.patch(f'/goals/goal/{goal.id}', data=update_data, content_type='application/json')
    assert response.status_code == 200
    assert response.data['title'] == 'new_test_goal'


@pytest.mark.django_db
def test_delete_goal_auth_user(create_goal):
    goal, client = create_goal

    response = client.delete(f'/goals/goal/{goal.id}')
    assert response.status_code == 204
