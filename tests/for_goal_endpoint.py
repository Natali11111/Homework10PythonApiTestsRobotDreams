import pytest
import pytest_check as check
from faker import Faker
from pytest_steps import test_steps

from models.methods_for_goal_endpoint import create_goal_with_all_fields, create_goal_with_name, update_goal_name, \
    get_goal, delete_goal, get_all_goals, create_goal_with_invalid_team_id, get_all_goals_with_invalid_team_id, \
    create_goal_with_invalid_body, create_goal_with_invalid_token, update_goal_name_with_invalid_token, \
    delete_goal_without_authorization_header, get_goal_with_invalid_token, \
    get_all_goals_with_invalid_token
from test_data.data_for_goal_endpoint import GoalTestData
from utils.GetTime import check_response_time_from_server


fake = Faker()

@pytest.mark.parametrize("name,description,color", GoalTestData.valid_body)
@test_steps("Create goal", "Get goal", "Delete goal")
def test_positive_create_goal(name, description,
                              color):
    response_post = create_goal_with_all_fields(name, description,
                                                color)
    data_from_post = response_post.json()
    id = data_from_post["goal"]["id"]
    assert response_post.status_code == 200
    check_response_time_from_server(response_post, "post")
    yield
    response_get = get_goal(id)
    data = response_get.json()
    check.equal(response_get.status_code, 200)
    check.equal(response_get.status_code, 200)
    check.equal(data["goal"]["name"], name)
    check.equal(data["goal"]["description"], description)
    check.equal(data["goal"]["color"], color)
    yield
    response_delete = delete_goal(id)
    assert response_delete.status_code == 200
    yield

@test_steps("Create goal", "Update goal", "Get goal", "Delete goal")
def test_positive_update_goal():
    updated_name = fake.name()
    response_post = create_goal_with_name(fake.name())
    assert response_post.status_code == 200
    data_from_post = response_post.json()
    id = data_from_post["goal"]["id"]
    yield
    response_put = update_goal_name(id, updated_name)
    assert response_put.status_code == 200
    check_response_time_from_server(response_put, "put")
    yield
    response_get = get_goal(id)
    data_from_get = response_get.json()
    assert response_get.status_code == 200
    assert data_from_get["goal"]["name"] == updated_name
    yield
    response_delete = delete_goal(id)
    assert response_delete.status_code == 200
    yield

@test_steps("Create goal", "Get goal", "Delete goal")
def test_positive_delete_goal():
    goal_name = fake.name()
    response_post = create_goal_with_name(goal_name)
    data_from_post = response_post.json()
    id = data_from_post["goal"]["id"]
    assert response_post.status_code == 200
    yield
    response_delete = delete_goal(id)
    assert response_delete.status_code == 200
    check_response_time_from_server(response_delete, "delete")
    yield
    response_get = get_goal(id)
    data_from_get = response_get.json()
    assert response_post.status_code == 404
    assert data_from_get["err"] == "Goal Not Found"
    yield

@test_steps("Create goals", "Get goals", "Delete goals")
def test_positive_get_all_goals():
    expected_first_goal_name = fake.name()
    expected_second_goal_name = fake.name()
    expected_third_goal_name = fake.name()
    actual_name_of_first_goal = create_goal_and_return_its_name(expected_first_goal_name)
    actual_name_of_second_goal = create_goal_and_return_its_name(expected_second_goal_name)
    actual_name_of_third_goal = create_goal_and_return_its_name(expected_third_goal_name)
    response = get_all_goals()
    assert response.status_code == 200
    yield
    check_response_time_from_server(response, "get")
    data = response.json()
    goals = data["goals"]
    assert len(goals) == 3
    assert goals[0]["name"] == actual_name_of_first_goal
    assert goals[1]["name"] == actual_name_of_second_goal
    assert goals[2]["name"] == actual_name_of_third_goal
    yield
    delete_goal(goals[0]["id"])
    delete_goal(goals[1]["id"])
    delete_goal(goals[2]["id"])

@pytest.mark.parametrize("team_id", GoalTestData.invalid_data_for_id)
def test_negative_create_goal_with_invalid_team_id(team_id):
    response = create_goal_with_invalid_team_id(fake.name(), fake.sentence(), fake.color(), team_id)
    data = response.json()
    check.equal(response.status_code, 400)
    check.equal(data["err"], "Invalid workspace id: " + str(team_id))

@pytest.mark.parametrize("goal_id", GoalTestData.invalid_data_for_id)
def test_negative_update_goal_with_invalid_goal_id(goal_id):
    response = update_goal_name(goal_id, fake.name())
    data = response.json()
    check.equal(response.status_code, 500)
    check.equal(data["err"], "Internal Server Error")

@pytest.mark.parametrize("goal_id", GoalTestData.invalid_data_for_id)
def test_negative_delete_goal_with_invalid_goal_id(goal_id):
    response = delete_goal(goal_id)
    data = response.json()
    check.equal(response.status_code, 500)
    check.equal(data["err"], "Internal Server Error")

@pytest.mark.parametrize("goal_id", GoalTestData.invalid_data_for_id)
def test_negative_delete_goal_with_invalid_goal_id(goal_id):
    response = get_goal(goal_id)
    data = response.json()
    check.equal(response.status_code, 500)
    check.equal(data["err"], "Internal Server Error")

@pytest.mark.parametrize("team_id", GoalTestData.invalid_data_for_id)
def test_negative_get_all_goals_with_invalid_team_id(team_id):
    response = get_all_goals_with_invalid_team_id(team_id)
    data = response.json()
    check.equal(response.status_code, 400)
    check.equal(data["err"], "Invalid workspace id: " + str(team_id))

@test_steps("Create goal", "Get goal", "Delete goal")
@pytest.mark.parametrize("token", GoalTestData.invalid_token)
def test_negative_get_goal_with_invalid_authorization_token(token):
    yield
    response_post = create_goal_with_all_fields(fake.name(), fake.sentence(), fake.color())
    data_from_post = response_post.json()
    id = data_from_post["goal"]["id"]
    assert response_post.status_code == 200
    yield
    response_get = get_goal_with_invalid_token(id, token)
    data_from_get = response_get.json()
    check.equal(data_from_get.status_code, 400)
    check.equal(data_from_post["err"], "Authorization header required")
    yield
    response_delete = delete_goal(id)
    assert response_delete.status_code == 200
    yield

@pytest.mark.parametrize("token", GoalTestData.invalid_token)
@test_steps("Create goals", "Get goals", "Delete goals")
def test_negative_get_all_goals_with_invalid_authorization_token(token):
    yield
    first_response_post = create_goal_with_name(fake.name())
    data_from_first_response = first_response_post.json()
    second_response_post = create_goal_with_name(fake.name())
    data_from_second_response = first_response_post.json()
    third_response_post = create_goal_with_name(fake.name())
    data_from_third_response = first_response_post.json()
    check.equal(first_response_post.status_code, 200)
    check.equal(second_response_post.status_code, 200)
    check.equal(third_response_post.status_code, 200)
    yield
    response_get = get_all_goals_with_invalid_token(token)
    data_from_get = response_get.json()
    check.equal(response_get.status_code, 400)
    check.equal(data_from_get["err"], "Authorization header required")
    yield
    response_first_delete = delete_goal(data_from_first_response["goal"]["id"])
    response_second_delete = delete_goal(data_from_second_response["goal"]["id"])
    response_third_delete = delete_goal(data_from_third_response["goal"]["id"])
    check.equal(response_first_delete.status_code, 200)
    check.equal(response_second_delete.status_code, 200)
    check.equal(response_third_delete.status_code, 200)
    yield


@pytest.mark.parametrize("token", GoalTestData.invalid_token)
def test_negative_create_goal_with_invalid_authorization_token(token):
    response = create_goal_with_invalid_token(fake.name(), fake.sentence(), fake.color(), token)
    data = response.json()
    check.equal(response.status_code, 400)
    check.equal(data["err"], "Authorization header required")


@pytest.mark.parametrize("token", GoalTestData.invalid_token)
@test_steps("Create goal", "Update goal", "Delete goal")
def test_negative_update_goal_with_invalid_authorization_token(token):
    yield
    response_post = create_goal_with_name(fake.name())
    assert response_post.status_code == 200
    data_from_post = response_post.json()
    id = data_from_post["goal"]["id"]
    yield
    response = update_goal_name_with_invalid_token(id, fake.name(), token)
    data = response.json()
    check.equal(response.status_code, 400)
    check.equal(data["err"], "Authorization header required")
    yield
    response_delete = delete_goal(id)
    assert response_delete.status_code == 200
    yield


@test_steps("Create goal", "Delete goal failed", "Delete goal passed")
def test_negative_delete_goal_without_authorization_header():
    yield
    response_post = create_goal_with_name(fake.name())
    assert response_post.status_code == 200
    data_from_post = response_post.json()
    id = data_from_post["goal"]["id"]
    yield
    response_delete = delete_goal_without_authorization_header(id)
    data_from_delete = response_delete.json()
    check.equal(response_delete.status_code, 400)
    check.equal(data_from_delete["err"], "Authorization header required")
    yield
    response_delete_second = delete_goal(id)
    assert response_delete_second.status_code == 200
    yield


@test_steps("Create goal", "Delete goal passed", "Delete goal failed")
def test_negative_delete_goal_two_times():
    yield
    response_post = create_goal_with_name(fake.name())
    assert response_post.status_code == 200
    data_from_post = response_post.json()
    id = data_from_post["goal"]["id"]
    yield
    response_delete = delete_goal(id)
    assert response_delete.status_code == 200
    yield
    response_second_delete = delete_goal(id)
    data_from_second_delete = response_second_delete.json()
    check.equal(response_second_delete.status_code, 404)
    check.equal(data_from_second_delete["err"], "Goal Not Found")
    yield


@pytest.mark.parametrize("description,color", GoalTestData.invalid_body)
def test_negative_create_goal_with_invalid_body(description, color):
    response = create_goal_with_invalid_body(description, color)
    data = response.json()
    check.equal(response.status_code, 500)
    check.equal(data["err"], "Internal Server Error")


def create_goal_and_return_its_name(goal_name):
    response_post = create_goal_with_name(goal_name)
    data_from_post = response_post.json()
    actual_name = data_from_post["goal"]["name"]
    return actual_name
