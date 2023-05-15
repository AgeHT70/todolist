import pytest


@pytest.mark.django_db
def test_create_comment_auth_user(create_goal):
    goal, client = create_goal
    comment_data = {'text': 'Test_comment', 'goal': goal.id, 'user': goal.user.id}
    response = client.post('/goals/goal_comment/create', data=comment_data, content_type='application/json')
    assert response.status_code == 201
    assert response.data['text'] == comment_data['text']


@pytest.mark.django_db
def test_update_comment_auth_user(create_comment):
    comment, client = create_comment
    update_data = {'text': 'new_test_comment'}
    response = client.patch(f'/goals/goal_comment/{comment.id}', data=update_data, content_type='application/json')
    assert response.status_code == 200
    assert response.data['text'] == update_data['text']


@pytest.mark.django_db
def test_delete_comment_auth_user(create_comment):
    comment, client = create_comment

    response = client.delete(f'/goals/goal_comment/{comment.id}')
    assert response.status_code == 204
