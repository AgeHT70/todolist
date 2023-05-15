import pytest

from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


@pytest.mark.django_db
@pytest.fixture
def get_user_data() -> dict[str, str]:
    user_data = {
        'username': 'test_username',
        'email': 'testemail@test.com',
        'password': 'test_password',
        'password_repeat': 'test_password',
    }
    return user_data


@pytest.mark.django_db
@pytest.fixture
def auth_user(client, django_user_model):
    user_data = {'username': 'test_username', 'password': 'test_password'}
    user = django_user_model.objects.create_user(**user_data)
    client.force_login(user)
    return client


@pytest.mark.django_db
@pytest.fixture
def board_create():
    data = {'title': 'test_board'}
    board = Board.objects.create(**data)
    return board


@pytest.mark.django_db
@pytest.fixture
def get_board_with_owner(client, django_user_model, board_create):
    board = board_create
    user_data = {'username': 'test_username', 'password': 'test_password'}
    user = django_user_model.objects.create_user(**user_data)
    BoardParticipant.objects.create(board=board, role=BoardParticipant.Role.owner, user=user)
    client.force_login(user)
    return board, client


@pytest.mark.django_db
@pytest.fixture
def create_category(client, board_create, django_user_model):
    board = board_create
    user_data = {'username': 'test_username', 'password': 'test_password'}
    user = django_user_model.objects.create_user(**user_data)
    category_data = {'title': 'Test_Category', 'board': board, 'user': user}
    BoardParticipant.objects.create(board=board, role=BoardParticipant.Role.owner, user=user)
    client.force_login(user)
    category = GoalCategory.objects.create(**category_data)

    return category, client


@pytest.mark.django_db
@pytest.fixture
def create_goal(client, create_category):
    category, client = create_category
    goal_data = {'title': 'Test_Goal', 'category': category, 'user': category.user}
    goal = Goal.objects.create(**goal_data)

    return goal, client


@pytest.mark.django_db
@pytest.fixture
def create_comment(client, create_goal):
    goal, client = create_goal
    comment_data = {'text': 'Test_comment', 'goal': goal, 'user': goal.user}
    comment = GoalComment.objects.create(**comment_data)

    return comment, client
